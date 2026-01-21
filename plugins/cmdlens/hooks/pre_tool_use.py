#!/usr/bin/env python3
"""CmdLens PreToolUse Hook

Parses risk level and recovery info from description field when Bash tool is called
and displays it via systemMessage to the user.
"""

import json
import re
import sys
import unicodedata


def get_display_width(text: str) -> int:
    """Calculate display width accounting for wide characters (emojis, CJK, etc.)."""
    width = 0
    for char in text:
        # East Asian Width: F(ull), W(ide) = 2, others = 1
        ea_width = unicodedata.east_asian_width(char)
        if ea_width in ('F', 'W'):
            width += 2
        # Emojis and other symbols often have width 2
        elif unicodedata.category(char) in ('So', 'Sk', 'Sm'):
            width += 2
        else:
            width += 1
    return width


def pad_to_width(text: str, target_width: int) -> str:
    """Pad text with spaces to reach target display width."""
    current_width = get_display_width(text)
    padding = target_width - current_width
    return text + " " * max(0, padding)


def parse_description(description: str) -> dict:
    """Parse description field and return structured information.

    Expected format: [RiskLevel] Description | Recovery: RecoveryMethod
    """
    result = {
        "risk_level": None,
        "explanation": None,
        "recovery": None
    }

    if not description:
        return result

    # Parse risk level: [Safe], [Caution], [Danger]
    risk_match = re.match(r'\[(Safe|Caution|Danger)\]\s*(.+)', description, re.IGNORECASE)
    if risk_match:
        result["risk_level"] = risk_match.group(1).capitalize()
        rest = risk_match.group(2)
    else:
        rest = description

    # Parse recovery info: | Recovery: ... or | 복구: ...
    recovery_match = re.search(r'\|\s*(?:Recovery|복구):\s*(.+)$', rest, re.IGNORECASE)
    if recovery_match:
        result["recovery"] = recovery_match.group(1).strip()
        rest = rest[:recovery_match.start()].strip()

    result["explanation"] = rest.strip() if rest.strip() else None

    return result


def get_risk_icon(risk_level: str | None) -> str:
    """Return icon for risk level."""
    icons = {
        "Safe": "🟢",
        "Caution": "🟡",
        "Danger": "🔴"
    }
    return icons.get(risk_level, "⚪")


def format_message(command: str, parsed: dict) -> str:
    """Format parsed info into a message for display."""
    # Truncate long commands (max 40 chars)
    if len(command) > 40:
        display_cmd = command[:37] + "..."
    else:
        display_cmd = command

    lines = ["", "┌─ 🔍 CmdLens ─────────────────────────────────"]
    lines.append(f"│ {display_cmd}")
    lines.append("├──────────────────────────────────────────────")

    if parsed["explanation"]:
        lines.append(f"│ 📋 {parsed['explanation']}")

    if parsed["risk_level"]:
        icon = get_risk_icon(parsed["risk_level"])
        lines.append(f"│ ⚠️  Risk: {icon} {parsed['risk_level']}")

    if parsed["recovery"]:
        lines.append(f"│ 💡 Recovery: {parsed['recovery']}")

    lines.append("└──────────────────────────────────────────────")

    return "\n".join(lines)


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Default behavior on JSON parse failure
        output = {"continue": True}
        print(json.dumps(output))
        return

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")
    description = tool_input.get("description", "")

    # Truncate long commands for display
    if len(command) > 40:
        display_cmd = command[:37] + "..."
    else:
        display_cmd = command

    # New format (starts with 📋): parse and display each part on separate lines
    if description.startswith("📋"):
        # Parse: 📋 desc | 🟢 Safe | 💡 Recovery: ...
        parts = [p.strip() for p in description.split("|")]
        desc_part = parts[0] if len(parts) > 0 else ""
        risk_part = parts[1] if len(parts) > 1 else ""
        recovery_part = parts[2] if len(parts) > 2 else ""

        # Format risk part
        if risk_part:
            risk_part = f"⚠️  Risk: {risk_part}"

        # Calculate max width for box
        content_lines = [display_cmd, desc_part, risk_part, recovery_part]
        content_lines = [l for l in content_lines if l]
        max_width = max(get_display_width(line) for line in content_lines)
        box_width = max_width + 2

        lines = [""]
        lines.append("┌─ 🔍 CmdLens " + "─" * (box_width - 11) + "┐")
        lines.append(f"│ {pad_to_width(display_cmd, max_width)} │")
        lines.append("├" + "─" * box_width + "┤")
        lines.append(f"│ {pad_to_width(desc_part, max_width)} │")
        if risk_part:
            lines.append(f"│ {pad_to_width(risk_part, max_width)} │")
        if recovery_part:
            lines.append(f"│ {pad_to_width(recovery_part, max_width)} │")
        lines.append("└" + "─" * box_width + "┘")
        message = "\n".join(lines)
    elif description:
        # Legacy format: parse and display
        parsed = parse_description(description)
        message = format_message(command, parsed)
    else:
        message = f"[CmdLens] Executing: {display_cmd}"

    output = {
        "continue": True,
        "systemMessage": message
    }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()

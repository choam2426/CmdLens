#!/usr/bin/env python3
"""CmdLens PreToolUse Hook

Bash 도구 호출 시 description 필드에서 위험도/복구 정보를 파싱하여
systemMessage로 사용자에게 표시합니다.
"""

import json
import re
import sys


def parse_description(description: str) -> dict:
    """description 필드를 파싱하여 구조화된 정보를 반환합니다.
    
    예상 형식: [위험도] 설명 | 복구: 복구방법
    """
    result = {
        "risk_level": None,
        "explanation": None,
        "recovery": None
    }
    
    if not description:
        return result
    
    # 위험도 파싱: [Safe], [Caution], [Danger]
    risk_match = re.match(r'\[(Safe|Caution|Danger)\]\s*(.+)', description, re.IGNORECASE)
    if risk_match:
        result["risk_level"] = risk_match.group(1).capitalize()
        rest = risk_match.group(2)
    else:
        rest = description
    
    # 복구 정보 파싱: | 복구: ... 또는 | Recovery: ...
    recovery_match = re.search(r'\|\s*(?:복구|Recovery):\s*(.+)$', rest, re.IGNORECASE)
    if recovery_match:
        result["recovery"] = recovery_match.group(1).strip()
        rest = rest[:recovery_match.start()].strip()
    
    result["explanation"] = rest.strip() if rest.strip() else None
    
    return result


def get_risk_icon(risk_level: str | None) -> str:
    """위험도에 맞는 아이콘을 반환합니다."""
    icons = {
        "Safe": "🟢",
        "Caution": "🟡",
        "Danger": "🔴"
    }
    return icons.get(risk_level, "⚪")


def format_message(command: str, parsed: dict) -> str:
    """파싱된 정보를 사용자에게 표시할 메시지로 포맷팅합니다."""
    lines = ["┌─ 🔍 CmdLens ─────────────────────────────────"]
    lines.append(f"│ {command}")
    lines.append("├──────────────────────────────────────────────")
    
    if parsed["explanation"]:
        lines.append(f"│ 📋 {parsed['explanation']}")
    
    if parsed["risk_level"]:
        icon = get_risk_icon(parsed["risk_level"])
        lines.append(f"│ ⚠️  위험도: {icon} {parsed['risk_level']}")
    
    if parsed["recovery"]:
        lines.append(f"│ 💡 복구: {parsed['recovery']}")
    
    lines.append("└──────────────────────────────────────────────")
    
    return "\n".join(lines)


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 기본 동작
        output = {"continue": True}
        print(json.dumps(output))
        return
    
    tool_input = hook_input.get("toolInput", {})
    command = tool_input.get("command", "")
    description = tool_input.get("description", "")
    
    # description이 있으면 파싱하여 표시
    if description:
        parsed = parse_description(description)
        message = format_message(command, parsed)
    else:
        # description이 없으면 명령어만 표시
        message = f"[CmdLens] 실행 예정: {command}"
    
    output = {
        "continue": True,
        "systemMessage": message
    }
    
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()

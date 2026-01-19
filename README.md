# CmdLens

**A cross-platform plugin that automatically explains commands before AI coding agents execute them.**

> Supported Platforms: Claude Code, Cursor, OpenCode.ai

---

## Example

When an AI agent tries to execute a command, CmdLens automatically displays an explanation:

```
┌─────────────────────────────────────────────────────┐
│ 🔍 CmdLens                                          │
├─────────────────────────────────────────────────────┤
│ find . -name "*.log" -mtime +7 -delete              │
├─────────────────────────────────────────────────────┤
│ 📋 This command:                                    │
│    Finds all .log files in the current directory   │
│    and subdirectories that are older than 7 days,  │
│    then deletes them.                              │
│                                                     │
│ ⚠️ Risk Level: Medium (🟡)                          │
│    • Files are permanently deleted (no trash)      │
│    • Applies recursively to all subdirectories     │
│                                                     │
│ 💡 Undo: Deleted files cannot be recovered.        │
│    Back up important files first.                  │
└─────────────────────────────────────────────────────┘
```

---

## Features

- **Automatic Command Explanation** — Explains every command before execution via hooks
- **Risk Level Indicator** — Visual risk assessment (🟢 Safe / 🟡 Caution / 🔴 Danger)
- **Undo Guide** — Shows how to reverse the action, or warns if irreversible
- **Multilingual Support** — Available in English and Korean

---

## Installation

> Coming soon — Installation instructions will be available after MVP release.

---

## How It Works

```
AI Agent decides to run a command
        ↓
Platform hook triggers (PreToolUse / beforeShellExecution)
        ↓
CmdLens analyzes the command via Claude Haiku API
        ↓
Explanation displayed to user
        ↓
User approves or rejects with full understanding
```

---

## Requirements

- Python 3.13+
- Anthropic API Key

---

## License

[Apache 2.0](LICENSE)

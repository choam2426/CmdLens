# CmdLens Description Guide

When using the Bash tool, write the **description** field in the following format.

## Format

```
📋 Description | ⚠️ Risk Level | 💡 Recovery: Recovery Method
```

## Risk Level Criteria and Icons

| Level | Icon | Description | Example Commands |
|-------|------|-------------|------------------|
| Safe | 🟢 | Read-only, information retrieval | `ls`, `cat`, `pwd`, `echo`, `git status` |
| Caution | 🟡 | File modification, config changes | `mv`, `cp`, `chmod`, `git commit` |
| Danger | 🔴 | File deletion, system changes, hard to undo | `rm -rf`, `sudo`, `dd`, `git push --force` |

## Writing Guidelines

### 📋 Description Writing Tips
- **Clearly explain what it does**
- **Mention target files/folders** if applicable
- **Briefly add the purpose** if relevant
- Examples:
  - ❌ `Delete file` (too simple)
  - ✅ `Delete cache files in temp folder to free up disk space`

### 💡 Recovery Method Writing Tips
- **Provide specific commands** (when possible)
- If recovery is impossible, **suggest alternatives/precautions**
- Examples:
  - ❌ `Not needed` (no information)
  - ✅ `Read-only operation, no recovery needed`
  - ❌ `Impossible`
  - ✅ `Deleted files cannot be recovered, backup recommended before execution`

## Examples

### Safe
```
📋 List files and folders in current directory | 🟢 Safe | 💡 Recovery: Read-only operation, no recovery needed
📋 Check Git repository status (changed files, staging status) | 🟢 Safe | 💡 Recovery: Read-only operation, no recovery needed
📋 View package.json contents to check dependencies | 🟢 Safe | 💡 Recovery: Read-only operation, no recovery needed
```

### Caution
```
📋 Move config.js file to backup folder | 🟡 Caution | 💡 Recovery: mv backup/config.js ./config.js
📋 Commit changes to Git to create version record | 🟡 Caution | 💡 Recovery: git reset HEAD~1 to undo commit
📋 Install npm package to add project dependency | 🟡 Caution | 💡 Recovery: npm uninstall <package-name> to remove
```

### Danger
```
📋 Delete entire node_modules folder for clean reinstall | 🔴 Danger | 💡 Recovery: npm install to reinstall, but takes time
📋 Force push to remote repository to overwrite history | 🔴 Danger | 💡 Recovery: Check git reflog for previous state recovery
📋 Modify system configuration file | 🔴 Danger | 💡 Recovery: Backup original before modification required, recovery may be difficult
```

## Rules

1. Write description for **all** Bash commands.
2. Risk level icon must be one of `🟢 Safe`, `🟡 Caution`, `🔴 Danger`.
3. Descriptions should be **specific and easy to understand**.
4. Recovery methods should provide **executable commands** or **specific methods**.
5. Write in the **user's language** (Korean/English).
6. For pipelines or compound commands, judge risk level based on the most dangerous part.

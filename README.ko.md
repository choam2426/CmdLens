# CmdLens

**명령어 실행 전 자동으로 설명해주는 Claude Code 플러그인**

> 모든 Bash 명령어에 위험도와 복구 방법을 표시합니다.

---

## 동작 예시

Claude가 명령어를 실행할 때, CmdLens가 표시합니다:

```
┌─ 🔍 CmdLens ─────────────────────────────────
│ find . -name "*.log" -mtime +7 -delete
├──────────────────────────────────────────────
│ 📋 7일 이상 된 .log 파일 찾아 삭제
│ ⚠️  위험도: 🔴 Danger
│ 💡 복구: 불가능, 백업 필요
└──────────────────────────────────────────────
```

---

## 주요 기능

- **자동 설명** — 모든 명령어에 위험도와 복구 정보 표시
- **위험도 표시** — 직관적인 위험 수준 (🟢 Safe / 🟡 Caution / 🔴 Danger)
- **복구 가이드** — 되돌리는 방법 또는 불가능 경고
- **다국어 지원** — 사용자 언어에 맞춰 설명 (한국어/영어)
- **의존성 없음** — 외부 API 호출 없음, 추가 패키지 불필요

---

## 설치 방법

### 방법 1: 마켓플레이스 (권장)

```bash
# 마켓플레이스 추가
/plugin marketplace add choam2426/CmdLens

# 플러그인 설치
/plugin install cmdlens@cmdlens-marketplace
```

### 방법 2: 수동 설치

1. 저장소 클론:

```bash
git clone https://github.com/choam2426/CmdLens.git
```

2. Claude Code 플러그인 디렉토리에 복사:

```bash
cp -r CmdLens/plugins/cmdlens ~/.claude/plugins/
```

3. Claude Code 재시작

---

## 작동 원리

```
세션 시작
      ↓
SessionStart 훅 → Claude에게 description 가이드 주입
      ↓
사용자 작업 요청
      ↓
Claude가 description 포함하여 Bash 명령어 준비
      ↓
PreToolUse 훅 → systemMessage로 위험도/복구 정보 표시
      ↓
명령어 실행
```

**융합 접근법:** SessionStart(동작 변경)와 PreToolUse(표시)를 결합하여 일관되고 안정적인 출력을 제공합니다.

---

## 위험도 기준

| 레벨 | 아이콘 | 설명 | 예시 |
|------|--------|------|------|
| Safe | 🟢 | 읽기 전용, 정보 조회 | `ls`, `cat`, `pwd`, `git status` |
| Caution | 🟡 | 파일 수정, 설정 변경 | `mv`, `cp`, `chmod`, `git commit` |
| Danger | 🔴 | 파일 삭제, 시스템 변경 | `rm -rf`, `sudo`, `git push --force` |

---

## 요구사항

- Python 3.10+
- Claude Code

---

## 프로젝트 구조

```
CmdLens/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── cmdlens/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── hooks/
│       │   ├── hooks.json
│       │   ├── session_start.py
│       │   └── pre_tool_use.py
│       └── prompts/
│           └── description_guide.md
├── docs/
│   └── PRD.md
└── README.md
```

---

## 라이선스

[MIT](LICENSE)

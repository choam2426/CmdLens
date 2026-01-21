# CmdLens PRD (Product Requirements Document)

> 버전: 0.3 (마켓플레이스 + 융합 접근법)  
> 최종 수정: 2026-01-21

---

## 1. 프로젝트 개요

**CmdLens**는 Claude Code가 터미널 명령어를 실행하기 전에, 해당 명령어가 무엇을 하는지 사용자에게 자동으로 설명해주는 플러그인입니다.

"Command Lens"의 줄임말로, 명령어를 렌즈로 들여다보듯 투명하게 보여준다는 의미를 담고 있습니다.

**v0.3 핵심 변경:**
- Claude Code 마켓플레이스 표준 구조 적용
- SessionStart + PreToolUse 융합 접근법 도입
- description 필드 기반 위험도/복구 정보 표시

---

## 2. 문제 정의

Claude Code는 강력한 코딩 에이전트이지만, 터미널에 익숙하지 않은 사용자에게 다음과 같은 문제가 발생합니다:

- 복잡한 명령어(파이프라인, 리다이렉션, 플래그 조합)의 의미 파악 어려움
- 명령어의 의미를 모른 채 "대충 승인" 또는 "무조건 거부"하는 양극단 선택
- AI 도구에 대한 신뢰 문제 발생
- 초보자의 진입 장벽 상승

**기존 보안 플러그인 vs CmdLens:**

| 기존 보안 플러그인 | CmdLens |
|-------------------|---------|
| 위험한 명령어 **차단** | 모든 명령어 **설명** |
| "이건 안 돼" | "이건 이런 걸 해, 알고 결정해" |
| 보안 중심 | 투명성 + 교육 중심 |

---

## 3. 목표

### v0.3 목표

1. Claude Code 마켓플레이스를 통한 간편 설치
2. SessionStart 훅으로 Claude 동작 변경 (description 가이드 주입)
3. PreToolUse 훅으로 systemMessage에 위험도/복구 정보 표시
4. 추가 API 호출 없이 동작 (비용 절감)

### 성공 지표

- 마켓플레이스에서 1-2줄 명령어로 설치 완료
- 모든 Bash 명령어 실행 전 위험도 표시
- 복구 방법 명확히 안내

---

## 4. 타겟 사용자

| 우선순위 | 사용자 그룹 | 특징 |
|---------|------------|------|
| 1차 | Claude Code 초보자 | 터미널에 익숙하지 않은 개발자 (주니어, 프론트엔드, 비전공) |
| 2차 | 투명성 중시 사용자 | AI 명령어를 명확히 파악하고 싶은 시니어/보안 담당자 |
| 3차 | 학습 목적 사용자 | Claude Code 사용하며 터미널 명령어를 배우려는 학생 |

---

## 5. 핵심 기능 (v0.3)

### 5.1 융합 접근법 아키텍처

```
세션 시작
    ↓
SessionStart 훅
    ↓
Claude에게 description 가이드 주입
    ↓
사용자 작업 요청
    ↓
Claude가 Bash 도구 호출 준비
    ↓
description 필드에 [위험도] 설명 | 복구: 방법 작성
    ↓
PreToolUse 훅 발동
    ↓
systemMessage로 사용자에게 정보 표시
    ↓
명령어 실행
```

### 5.2 위험도 표시

| 레벨 | 아이콘 | 설명 | 예시 |
|-----|-------|------|-----|
| Safe | 🟢 | 읽기 전용, 정보 조회 | `ls`, `cat`, `pwd`, `echo`, `git status` |
| Caution | 🟡 | 파일 수정, 설정 변경 | `mv`, `cp`, `chmod`, `git commit` |
| Danger | 🔴 | 파일 삭제, 시스템 변경 | `rm -rf`, `sudo`, `dd`, `git push --force` |

### 5.3 되돌리기 가이드

- 복구 가능한 작업: 구체적 복구 명령어 안내
- 복구 불가능한 작업: "불가능, 백업 필요" 명시

### 5.4 다국어 지원

- Claude가 사용자의 언어(한국어/영어)에 맞춰 자동으로 설명 생성

---

## 6. 기술 스택

| 구분 | 기술 |
|-----|------|
| 언어 | Python 3.10+ |
| 플랫폼 | Claude Code Plugin (마켓플레이스) |
| 훅 | SessionStart + PreToolUse |
| 의존성 | 없음 (표준 라이브러리만 사용) |

---

## 7. 디렉토리 구조

```
CmdLens/
├── .claude-plugin/
│   └── marketplace.json          # 마켓플레이스 manifest
├── plugins/
│   └── cmdlens/
│       ├── .claude-plugin/
│       │   └── plugin.json       # 플러그인 manifest
│       ├── hooks/
│       │   ├── hooks.json        # 훅 정의
│       │   ├── session_start.py  # SessionStart 훅
│       │   └── pre_tool_use.py   # PreToolUse 훅
│       └── prompts/
│           └── description_guide.md  # description 작성 가이드
├── docs/
│   └── PRD.md
├── .gitignore
├── LICENSE
├── README.md
└── README.ko.md
```

---

## 8. Hook 스키마

### 8.1 hooks.json

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py\"",
        "timeout": 5000
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/pre_tool_use.py\"",
        "timeout": 3000
      }]
    }]
  }
}
```

### 8.2 SessionStart 출력

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "# CmdLens Description Guide\n\nBash 도구 사용 시..."
  }
}
```

### 8.3 PreToolUse 출력

```json
{
  "continue": true,
  "systemMessage": "┌─ 🔍 CmdLens ─────────────────────────────────\n│ ls -la\n..."
}
```

---

## 9. UI/UX

### 9.1 출력 형식

PreToolUse 훅이 systemMessage로 다음 형식을 표시합니다:

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

## 10. 제약 사항 및 예외 처리

### 10.1 description 미사용

Claude가 description 필드를 사용하지 않을 경우:
- 기본 메시지 표시: "[CmdLens] 실행 예정: {command}"

### 10.2 파싱 실패

description 형식이 맞지 않을 경우:
- 가능한 정보만 추출하여 표시
- 파싱 불가 시 원본 description 그대로 표시

### 10.3 Python 미설치

- 요구사항에 Python 3.10+ 명시
- 설치 가이드 제공

---

## 11. 향후 확장 (v0.4+)

| 기능 | 설명 |
|-----|------|
| 위험도별 동작 | Danger 명령어는 추가 확인 요청 |
| 제외 목록 | 신뢰하는 명령어 패턴 스킵 (`git status`, `ls`) |
| Cursor 지원 | beforeShellExecution 훅 연동 |
| 통계 대시보드 | 실행된 명령어 위험도 분포 시각화 |

---

## 12. 변경 이력

| 버전 | 날짜 | 주요 변경 |
|-----|------|----------|
| 0.1 | 2026-01-20 | 초기 설계 (PreToolUse 방식) |
| 0.2 | 2026-01-21 | SessionStart 방식으로 전환 |
| 0.3 | 2026-01-21 | 마켓플레이스 구조 + 융합 접근법 |

---

*이 문서는 개발 기준이며, 진행에 따라 업데이트됩니다.*

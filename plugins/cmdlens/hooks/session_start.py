#!/usr/bin/env python3
"""CmdLens SessionStart Hook

Claude Code 세션 시작 시 additionalContext를 주입하여
Bash 도구의 description 필드에 위험도/복구 정보를 포함하도록 지시합니다.
"""

import json
import os
from pathlib import Path


def main() -> None:
    # 플러그인 루트 경로 (환경변수 또는 파일 위치 기준)
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if plugin_root:
        prompt_path = Path(plugin_root) / "prompts" / "description_guide.md"
    else:
        # fallback: 스크립트 위치 기준
        hook_dir = Path(__file__).parent
        prompt_path = hook_dir.parent / "prompts" / "description_guide.md"

    # 프롬프트 파일 읽기
    if prompt_path.exists():
        prompt = prompt_path.read_text(encoding="utf-8")
    else:
        # fallback: 기본 프롬프트
        prompt = """# CmdLens Description Guide

Bash 도구 사용 시 description 필드를 다음 형식으로 작성하세요:

[위험도] 설명 | 복구: 복구방법

예시:
- [Safe] 현재 디렉토리 파일 목록 조회 | 복구: 불필요
- [Caution] 파일 이동 | 복구: mv target source
- [Danger] 디렉토리 삭제 | 복구: 불가능, 백업 필요"""

    # SessionStart 훅 출력 형식
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": prompt
        }
    }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()

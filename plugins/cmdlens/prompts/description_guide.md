# CmdLens Description Guide

Bash 도구를 사용할 때 **description** 필드에 다음 형식으로 작성하세요.

## 형식

```
[위험도] 설명 | 복구: 복구방법
```

## 위험도 기준

| 레벨 | 설명 | 예시 명령어 |
|------|------|-------------|
| Safe | 읽기 전용, 정보 조회 | `ls`, `cat`, `pwd`, `echo`, `git status` |
| Caution | 파일 수정, 설정 변경 | `mv`, `cp`, `chmod`, `git commit` |
| Danger | 파일 삭제, 시스템 변경, 되돌리기 어려움 | `rm -rf`, `sudo`, `dd`, `git push --force` |

## 예시

### Safe (안전)
```
[Safe] 현재 디렉토리 파일 목록 조회 | 복구: 불필요
[Safe] Git 상태 확인 | 복구: 불필요
[Safe] 파일 내용 출력 | 복구: 불필요
```

### Caution (주의)
```
[Caution] 파일 이동: source.txt → dest.txt | 복구: mv dest.txt source.txt
[Caution] 파일 복사 (기존 파일 덮어쓰기 가능) | 복구: 원본 유지됨
[Caution] 패키지 설치 | 복구: pip uninstall <package>
```

### Danger (위험)
```
[Danger] 디렉토리 전체 삭제 | 복구: 불가능, 백업 필요
[Danger] 원격 저장소에 강제 푸시 | 복구: git reflog로 복구 시도 가능
[Danger] 시스템 설정 변경 | 복구: 변경 전 설정값 기록 필요
```

## 규칙

1. **모든** Bash 명령어에 description을 작성합니다.
2. 위험도는 반드시 `[Safe]`, `[Caution]`, `[Danger]` 중 하나를 사용합니다.
3. 복구 방법은 구체적으로 작성합니다 (불가능한 경우 "불가능" 명시).
4. 사용자의 언어(한국어/영어)에 맞춰 작성합니다.
5. 파이프라인이나 복합 명령어는 가장 위험한 부분 기준으로 위험도를 판단합니다.

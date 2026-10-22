# 델파이 코드 조각 익명화 도구 (Python GUI)

델파이(Object Pascal) 코드 조각을 붙여넣으면, 함수명/변수명/필드명/문자열 리터럴/주석을
가명(`ID1`, `STR1` ...)으로 바꿔주는 로컬 GUI 도구입니다.

모든 처리는 내 컴퓨터 안에서만 일어나고, 어디로도 전송되지 않습니다.

## 구성 파일

| 파일 | 역할 |
|---|---|
| `engine.py` | 실제 치환 로직 (순수 함수, 화면/로그를 전혀 모름) |
| `logger.py` | 실행할 때마다 `anonymize_log.txt`에 기록(추적용) |
| `app.py` | Tkinter GUI, 실행 진입점 |
| `requirements.txt` | 의존 패키지 안내 (현재 외부 pip 패키지 없음) |

네 파일을 전부 같은 폴더에 둔 상태로 실행해야 합니다.

## 1. 사전 준비

파이썬 3.8 이상이 설치되어 있어야 합니다. 터미널에서 버전 확인:

```bash
python3 --version
```

**리눅스(Ubuntu/Debian)** 사용자는 `tkinter`가 기본 파이썬에 포함되어 있지 않을 수 있습니다.
먼저 아래 명령으로 시스템에 설치해주세요 (윈도우/맥은 보통 생략 가능).

```bash
sudo apt-get install python3-tk
```

맥(Homebrew 파이썬)이라면:

```bash
brew install python-tk
```

## 2. 가상환경(venv) 만들기

이 폴더(`delphi_anonymizer_pygui/`)로 이동한 뒤:

```bash
cd delphi_anonymizer_pygui
python3 -m venv venv
```

가상환경 활성화:

```bash
# Windows (cmd)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

활성화되면 터미널 프롬프트 앞에 `(venv)`가 붙습니다.

## 3. 의존성 설치

```bash
pip install -r requirements.txt
```

`requirements.txt`에는 설치할 외부 패키지가 없습니다(표준 라이브러리만 사용). 이 명령은 형식상 실행해도 되고 생략해도 됩니다.

## 4. 실행

```bash
python app.py
```

GUI 창이 뜨면 됩니다.

## 5. 사용 방법

1. 위쪽 "입력" 칸에 익명화하고 싶은 코드 조각을 붙여넣습니다.
2. "익명화하기"를 누릅니다.
3. 왼쪽 아래 "결과" 칸에 안전하게 공유 가능한 코드가 나타납니다. "결과 복사" 버튼으로 바로 복사할 수 있습니다.
4. 오른쪽 "매핑표"에는 가명과 실제 값이 쌍으로 표시됩니다. **이 표는 본인만 확인하고 절대 외부(예: Claude)로 전달하지 마세요.**
5. 실행할 때마다 같은 폴더의 `anonymize_log.txt`에 실행 기록(시각, run id, 전체 매핑)이 자동으로 쌓입니다. "로그 파일 보기" 버튼으로 전체 로그를 확인할 수 있습니다.
6. 라이브러리 이름(예: 사내 공용 유틸 함수)인데 자동으로 가려졌다면, "가리지 않을 이름" 입력란에 쉼표로 구분해서 추가하고 다시 실행하세요.

## 주의사항

- `anonymize_log.txt`와 GUI의 "매핑표"에는 **원본 이름이 그대로 보존**됩니다. 공유 금지, 본인 컴퓨터에만 보관하세요.
- 공유해도 되는 건 왼쪽 "결과" 칸의 내용뿐입니다.
- 자동 치환이 완벽하지 않을 수 있으니, 보내기 전에 결과를 한 번 훑어보고 혹시 남은 민감한 이름이 있는지 확인하세요.

## 종료 / 재실행

가상환경을 끌 때는:

```bash
deactivate
```

다음에 다시 쓸 때는 가상환경 활성화(2번 단계) 후 바로 `python app.py`만 실행하면 됩니다(`pip install`은 최초 1회면 충분).

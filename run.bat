@echo off
setlocal
cd /d %~dp0

:: 1. 가상환경 폴더 존재 확인
if not exist ".venv" (
    echo [INFO] Make new .venv environment... (Just 1 time)
    python -m venv .venv
)

:: 2. 가상환경 활성화
call .venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;%~dp0src

:: 3. 의존성 설치 (필요시 업데이트)
:: - 전송 속도를 위해 requirements.txt가 수정된 경우에만 설치하게 할 수도 있지만, 
::   간단하게 매번 체크(빠름)하게 구성합니다.
echo [INFO] Confirm the dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. 실행 (창 없이 실행하려면 pythonw 사용)
echo [INFO] Start the app.
start /b "" pythonw src\main.py

exit
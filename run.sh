#!/bin/bash

# 현재 경로로 이동
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

# 1. 가상환경 폴더 존재 확인
if [ ! -d ".venv" ]; then
    echo "[INFO] Make new .venv environment... (Just 1 time)"
    python3 -m venv .venv
fi

# 2. 가상환경 활성화
source .venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# 3. 의존성 설치
echo "[INFO] Confirm the dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. 실행
echo "[INFO] Start the app."
python src/main.py

exit
#!/bin/bash
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:$PATH"

PROJ_DIR="$(dirname "$(realpath "$0")")"
cd "$PROJ_DIR"

# Appium 서버 실행 확인 및 자동 시작
if ! curl -s http://localhost:4723/status > /dev/null 2>&1; then
    appium &
    sleep 5
fi

source .venv/bin/activate
python3 -m pytest tests/test_refund.py tests/test_cash_receipt.py -v --slack

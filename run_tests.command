#!/bin/bash
cd "$(dirname "$0")"

# Appium 서버 실행 확인 및 자동 시작
if ! curl -s http://localhost:4723/status > /dev/null 2>&1; then
    osascript -e 'tell application "Terminal" to do script "appium"'
    echo "Appium 서버 시작 중... (5초 대기)"
    sleep 5
fi

# 테스트 선택 다이얼로그
choice=$(osascript <<EOF
choose from list {"결제+환불 전체 (Slack 전송)", "결제+환불 전체", "카드 결제만", "현금 결제만", "앱 실행 확인"} with prompt "실행할 테스트를 선택하세요:" default items {"결제+환불 전체 (Slack 전송)"}
EOF
)

if [ "$choice" = "false" ] || [ -z "$choice" ]; then
    exit 0
fi

source .venv/bin/activate

echo ""
echo "========================================="
echo " 선택: $choice"
echo "========================================="
echo ""

case "$choice" in
    "결제+환불 전체 (Slack 전송)")
        python3 -m pytest tests/test_refund.py -v --slack
        ;;
    "결제+환불 전체")
        python3 -m pytest tests/test_refund.py -v
        ;;
    "카드 결제만")
        python3 -m pytest tests/test_card_payment.py -v
        ;;
    "현금 결제만")
        python3 -m pytest tests/test_cash_payment.py -v
        ;;
    "앱 실행 확인")
        python3 -m pytest tests/test_launch_app.py tests/test_select_appium_category.py -v
        ;;
esac

echo ""
echo "테스트 완료. 창을 닫으려면 아무 키나 누르세요."
read -n 1

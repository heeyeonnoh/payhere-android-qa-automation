# payhere-android-qa-automation

Android 실기기 기반 QA 자동화 테스트 프로젝트 (Appium + pytest)

---

## 사전 준비

| 항목 | 버전 | 설치 방법 |
|------|------|-----------|
| Python | 3.10 이상 | https://python.org |
| Node.js | 18 이상 | https://nodejs.org |
| Appium | 2.x | `npm install -g appium` |
| Appium UiAutomator2 드라이버 | - | `appium driver install uiautomator2` |
| Android SDK (adb) | - | Android Studio 또는 `brew install android-platform-tools` |
| Allure | - | `brew install allure` |

---

## 환경 설정

### 1. 레포 클론

```bash
git clone https://github.com/heeyeonnoh/payhere-android-qa-automation.git
cd payhere-android-qa-automation
```

### 2. 가상환경 생성 및 패키지 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일 생성:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### 4. Android 기기 연결

- 기기에서 **USB 디버깅** 활성화 (설정 → 개발자 옵션)
- USB로 맥에 연결 후 아래 명령으로 인식 확인

```bash
adb devices
```

---

## 실행 방법

### 방법 1: 더블클릭으로 실행 (권장)

`run_tests.command` 파일을 더블클릭하면 아래 다이얼로그가 나타납니다.

> 처음 실행 시 macOS 보안 경고가 뜨면:  
> **시스템 설정 → 개인 정보 보호 및 보안 → "확인 없이 열기"** 클릭

선택 가능한 옵션:
- **결제+환불 전체 (Slack 전송)** — 6개 테스트 실행 후 Slack 알림
- **결제+환불 전체** — Slack 전송 없이 실행
- **카드 결제만**
- **현금 결제만**
- **앱 실행 확인**

> Appium 서버가 꺼져 있으면 자동으로 실행됩니다.

---

### 방법 2: 터미널 직접 실행

**Appium 서버 먼저 실행** (별도 터미널):

```bash
appium
```

**테스트 실행:**

```bash
source .venv/bin/activate

# 결제+환불 전체 (Slack 알림 포함)
python3 -m pytest tests/test_refund.py -v --slack

# 결제+환불 전체 (Slack 없이)
python3 -m pytest tests/test_refund.py -v

# 카드 결제만
python3 -m pytest tests/test_card_payment.py -v

# 현금 결제만
python3 -m pytest tests/test_cash_payment.py -v
```

---

## 테스트 구성

| 파일 | 내용 |
|------|------|
| `tests/test_refund.py` | 결제 후 환불 세트 6개 (카드/현금 × 미만/50k/이상) |
| `tests/test_card_payment.py` | 카드 결제 3개 (환불 없음) |
| `tests/test_cash_payment.py` | 현금 결제 3개 (환불 없음) |
| `tests/test_launch_app.py` | 앱 실행 확인 |
| `tests/test_select_appium_category.py` | 카테고리 선택 확인 |

---

## 자동 스케줄 실행 (crontab)

매일 정해진 시간에 자동으로 테스트를 실행하려면 crontab을 등록합니다.

```bash
cd payhere-android-qa-automation
SCRIPT="$(pwd)/run_scheduled.sh"
LOG="$(pwd)/cron.log"
(crontab -l 2>/dev/null; echo "0 9 * * * $SCRIPT >> $LOG 2>&1"; echo "0 13 * * * $SCRIPT >> $LOG 2>&1") | crontab -
```

위 명령은 **매일 오전 9시 / 오후 1시**에 결제+환불 전체 테스트를 실행하고 Slack으로 결과를 전송합니다.

> **주의:** 맥이 절전 상태면 실행되지 않습니다. 시스템 설정 → 배터리 → 절전 방지를 켜두세요.

등록 확인:
```bash
crontab -l
```

실행 로그 확인:
```bash
cat cron.log
```

---

## Allure 리포트

테스트 실행 후 로컬에서 리포트 확인:

```bash
allure serve allure-results
```

`--slack` 플래그 사용 시 GitHub Pages에 자동 배포되고 Slack에 링크가 전송됩니다.

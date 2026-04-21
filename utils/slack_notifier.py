import urllib.request
import json
import ssl
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]


def send_test_results(passed: int, failed: int, error: int, duration: float, failures: list[str], report_url: str = None):
    total = passed + failed + error
    status = "SUCCESS" if failed == 0 and error == 0 else "FAILURE"

    lines = [
        f":robot_face: Android QA 테스트 결과",
        "──────────────────",
        f":calendar: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f":white_check_mark: 성공 {passed} / :x: 실패 {failed + error} / 전체 {total}",
        f":stopwatch: 소요시간: {duration:.1f}초",
    ]

    if failures:
        lines.append("\n실패 항목:")
        for name in failures:
            lines.append(f"  • {name}")

    if report_url:
        lines.append(f"\n:bar_chart: <{report_url}|Allure 리포트 보기>")

    payload = {"text": "\n".join(lines)}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    urllib.request.urlopen(req, context=ctx)

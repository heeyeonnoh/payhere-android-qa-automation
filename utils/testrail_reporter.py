import urllib.request
import json
import ssl
import base64
import os
from dotenv import load_dotenv

load_dotenv()

TESTRAIL_URL      = os.environ.get("TESTRAIL_URL", "https://payhere.testrail.io")
TESTRAIL_USERNAME = os.environ.get("TESTRAIL_USERNAME", "heeyeon.noh@payhere.in")
TESTRAIL_API_KEY  = os.environ.get("TESTRAIL_API_KEY", "")

# pytest 테스트 함수명 → TestRail case_id 매핑
CASE_MAP: dict[str, int] = {
    # 카드 결제
    "test_card_payment_under_50k":               301985,
    "test_card_payment_50k":                     301985,
    "test_card_payment_over_50k":                301985,
    "test_card_payment_50k_installment_2m":      301991,
    "test_card_payment_over_50k_installment_2m": 301991,
    # 현금 결제
    "test_cash_payment_under_50k":               301986,
    "test_cash_payment_50k":                     301986,
    "test_cash_payment_over_50k":                301986,
    # 현금영수증
    "test_cash_payment_with_receipt_and_refund":          301939,
    "test_cash_payment_with_business_receipt_and_refund": 301940,
    # 환불
    "test_card_payment_under_50k_and_refund":            301942,
    "test_card_payment_50k_and_refund":                  301942,
    "test_card_payment_over_50k_and_refund":             301942,
    "test_card_payment_50k_installment_and_refund":      301942,
    "test_card_payment_over_50k_installment_and_refund": 301942,
    "test_cash_payment_under_50k_and_refund":            301943,
    "test_cash_payment_50k_and_refund":                  301943,
    "test_cash_payment_over_50k_and_refund":             301943,
    # 분할결제
    "test_split_cash_card_and_refund": 301933,
    "test_split_card_card_and_refund": 301932,
    # 더치페이
    "test_dutch_pay_cash_card_and_refund": 301920,
    # 쿠폰
    "test_coupon_card_payment_and_refund": 302008,
    "test_coupon_cash_payment_and_refund": 302008,
    # 포인트
    "test_points_card_payment_and_refund": 302002,
    "test_points_cash_payment_and_refund": 302002,
}

STATUS_PASSED = 1
STATUS_FAILED = 5


def _api(method: str, path: str, body: dict = None):
    creds = base64.b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_API_KEY}".encode()).decode()
    url = f"{TESTRAIL_URL}/index.php?/api/v2/{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"},
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def report_results(run_id: int, test_results: dict[str, bool], failure_reasons: dict[str, str]):
    """주어진 run_id에 테스트 결과 업데이트.
    한 case_id에 여러 테스트가 매핑된 경우, 하나라도 실패하면 Failed."""
    case_status: dict[int, int] = {}
    case_comments: dict[int, list[str]] = {}

    for test_name, passed in test_results.items():
        case_id = CASE_MAP.get(test_name)
        if case_id is None:
            continue
        if case_id not in case_status:
            case_status[case_id] = STATUS_PASSED
            case_comments[case_id] = []

        if not passed:
            case_status[case_id] = STATUS_FAILED
            reason = failure_reasons.get(test_name, "")
            case_comments[case_id].append(f"❌ {test_name}: {reason}")
        else:
            case_comments[case_id].append(f"✅ {test_name}")

    if not case_status:
        print("업데이트할 케이스 없음 (매핑된 테스트 결과 없음)")
        return

    results = [
        {"case_id": cid, "status_id": status, "comment": "\n".join(case_comments[cid])}
        for cid, status in case_status.items()
    ]
    _api("POST", f"add_results_for_cases/{run_id}", {"results": results})
    print(f"업데이트 완료: {len(results)}개 케이스 → Run {run_id}")
    for r in results:
        icon = "✅" if r["status_id"] == STATUS_PASSED else "❌"
        print(f"  {icon} C{r['case_id']}")

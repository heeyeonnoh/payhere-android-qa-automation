"""
사용법: python3 update_testrail.py <run_id 또는 TestRail 링크>
예시:
  python3 update_testrail.py 10184
  python3 update_testrail.py https://payhere.testrail.io/index.php?/runs/view/10184
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.testrail_reporter import report_results

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(REPO_DIR, "last_test_results.json")


def extract_run_id(arg: str) -> int:
    # URL에서 run_id 추출
    m = re.search(r'/runs/view/(\d+)', arg)
    if m:
        return int(m.group(1))
    # 숫자만 입력한 경우
    if arg.isdigit():
        return int(arg)
    raise ValueError(f"run_id를 파싱할 수 없습니다: {arg}")


if len(sys.argv) < 2:
    print("사용법: python3 update_testrail.py <run_id 또는 링크>")
    sys.exit(1)

run_id = extract_run_id(sys.argv[1])

if not os.path.exists(RESULTS_FILE):
    print(f"마지막 테스트 결과 파일이 없습니다: {RESULTS_FILE}")
    print("테스트를 먼저 실행해주세요.")
    sys.exit(1)

with open(RESULTS_FILE, encoding="utf-8") as f:
    data = json.load(f)

print(f"테스트 실행 시각: {data.get('run_at', '알 수 없음')}")
print(f"Run ID: {run_id} 업데이트 중...\n")

report_results(run_id, data["test_results"], data.get("failure_reasons", {}))

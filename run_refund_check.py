import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.conftest import _check_and_refund_unrefunded_payments

print("미환불 거래 확인 및 자동 환불 시작...")
auto_refunded, still_unrefunded = _check_and_refund_unrefunded_payments()

print("\n===== 결과 =====")
if auto_refunded is None:
    print("기기/Appium 연결 실패로 확인 불가")
else:
    if auto_refunded:
        print(f"자동 환불 완료 ({len(auto_refunded)}건):")
        for item in auto_refunded:
            print(f"  - {item}")
    else:
        print("자동 환불 건 없음")

    if still_unrefunded:
        print(f"\n⚠️  환불 실패 (아직 미환불, {len(still_unrefunded)}건):")
        for item in still_unrefunded:
            print(f"  - {item}")
    else:
        print("모든 거래 환불 완료")

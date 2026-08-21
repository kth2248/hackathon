# offline_test.py
"""
대회 전날, Wi-Fi를 완전히 끈 상태에서 반드시 실행할 것.
여기서 실패하면 당일 대응 시간이 필요하므로 최우선으로 검증한다.
"""
import sys
import os
for _cat in ("vectors", "scene", "ui"):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", _cat))

print("=== 1. 자체 라이브러리 import 테스트 (오프라인 무관, 항상 성공해야 정상) ===")
try:
    from vector_helpers import direction_to, distance, avoid_vector, clamp_speed, blend_vectors
    print("✅ vector_helpers import 성공")
except ImportError as e:
    print(f"❌ vector_helpers import 실패: {e}")

try:
    from vpython_utils import make_scene, make_agent, make_obstacle, make_floor
    print("✅ vpython_utils import 성공")
except ImportError as e:
    print(f"❌ vpython_utils import 실패: {e}")

try:
    from ui_widgets import make_labeled_slider, make_toggle
    print("✅ ui_widgets import 성공")
except ImportError as e:
    print(f"❌ ui_widgets import 실패: {e}")

print("\n=== 2. VPython 렌더링 테스트 (인터넷 필요 여부 확인, 핵심 검증) ===")
try:
    from vpython import sphere, vector, color
    ball = sphere(pos=vector(0, 0, 0), radius=1, color=color.red)
    print("✅ VPython 렌더링 성공 — 브라우저 창이 실제로 떴는지 육안 확인 필수")
except Exception as e:
    print(f"❌ VPython 렌더링 실패 (인터넷 필요 가능성 있음): {e}")

print("\n=== 3. 간단 애니메이션 루프 테스트 (rate() 정상 동작 확인) ===")
try:
    from vpython import rate
    import time
    start = time.time()
    frames = 0
    while time.time() - start < 1:  # 1초만 테스트
        rate(60)
        frames += 1
    print(f"✅ rate(60) 루프 정상 동작, 1초간 {frames} 프레임 처리됨")
except Exception as e:
    print(f"❌ 애니메이션 루프 실패: {e}")

print("\n체크리스트 완료. ❌가 하나라도 있으면 대회 전날 안에 원인 파악 및 대안(matplotlib 폴백 등) 준비할 것.")

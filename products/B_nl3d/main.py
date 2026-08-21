# main.py — B안: 자연어로 조종하는 3D 창작 도구
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작 — 오프라인 파서가 기본)
#
# 2단 구조:
#   1단계(필수, 오프라인): 키워드 사전 + 정규식 규칙 파서 — 항상 동작
#   2단계(선택, 온라인):   Claude API 자유 문장 해석 — 실패 시 자동 오프라인 폴백
#
# 재사용 부품: vpython_utils(make_scene)

import os
import sys
import re
import math

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import sphere, box, vector, color, winput, wtext, rate
from vpython_utils import make_scene

# ============================================================
# 1단계: 규칙 기반 파서 (오프라인, 항상 동작해야 함)
# ============================================================
# 발표 전 실제로 말할 문장의 단어들을 여기에 미리 다 넣어둘 것.
COLOR_MAP = {
    "빨간": color.red, "빨강": color.red, "레드": color.red,
    "파란": color.blue, "파랑": color.blue, "블루": color.blue,
    "초록": color.green, "녹색": color.green, "그린": color.green,
    "노란": color.yellow, "노랑": color.yellow,
    "주황": color.orange, "오렌지": color.orange,
    "보라": color.purple, "자주": color.purple,
    "하늘": color.cyan, "청록": color.cyan,
    "하양": color.white, "흰": color.white,
    "검정": color.black, "검은": color.black,
}

SHAPE_MAP = {
    "구": sphere, "공": sphere, "행성": sphere, "볼": sphere,
    "박스": box, "상자": box, "큐브": box, "정육면체": box, "블록": box,
}

MAX_COUNT = 40   # 성능 보호: 너무 많은 개수 요청 방지


def parse_command_offline(text):
    """규칙 기반 파서: "빨간 구 3개를 나선으로 배치해줘" 같은 문장에서
    색상/모양/개수/배치 패턴을 정규식과 키워드 매칭으로 추출한다.
    Claude API 없이도 항상 동작하는 게 핵심.
    """
    color_obj = color.white
    for kor, c in COLOR_MAP.items():
        if kor in text:
            color_obj = c
            break

    shape_cls = sphere
    for kor, cls in SHAPE_MAP.items():
        if kor in text:
            shape_cls = cls
            break

    count_match = re.search(r"(\d+)\s*개", text)
    count = int(count_match.group(1)) if count_match else 1
    count = max(1, min(count, MAX_COUNT))

    if "나선" in text or "spiral" in text:
        pattern = "spiral"
    elif "원" in text or "circle" in text or "동그라" in text:
        pattern = "circle"
    else:
        pattern = "line"

    return {"color": color_obj, "shape": shape_cls, "count": count, "pattern": pattern}


# ============================================================
# 2단계 (선택): Claude API로 자유 문장 해석
# ============================================================
def parse_command_with_api(text):
    """API 키가 있고 인터넷이 될 때만 사용. 실패하면 반드시 오프라인 파서로 폴백.
    (실제 API 호출은 온라인 확인 후 별도 구현 — 대회 기본값은 오프라인 파서.)
    """
    try:
        raise NotImplementedError("API 연동은 온라인 확인 후 별도 구현")
    except Exception:
        return parse_command_offline(text)   # 실패 시 반드시 폴백


# ============================================================
# 3. 렌더링
# ============================================================
generated = []   # 이번에 생성한 객체들(다시 입력하면 지우고 새로 그림)


def clear_generated():
    global generated
    for obj in generated:
        obj.visible = False
    generated = []


def make_position(i, spec):
    """배치 패턴에 따라 i번째 객체의 위치를 계산."""
    n = spec["count"]
    if spec["pattern"] == "spiral":
        angle = i * 1.2
        r = 1 + i * 0.4
        return vector(math.cos(angle) * r, math.sin(angle) * r, i * 0.3)
    if spec["pattern"] == "circle":
        angle = (2 * math.pi / n) * i
        r = 1 + n * 0.15
        return vector(math.cos(angle) * r, math.sin(angle) * r, 0)
    # line
    return vector(i * 1.2 - n * 0.6, 0, 0)


def render_scene(spec):
    """파싱된 spec(dict)을 받아 실제 3D 객체들을 생성한다."""
    clear_generated()
    for i in range(spec["count"]):
        pos = make_position(i, spec)
        if spec["shape"] is box:
            obj = box(pos=pos, size=vector(0.7, 0.7, 0.7), color=spec["color"])
        else:
            obj = sphere(pos=pos, radius=0.4, color=spec["color"])
        generated.append(obj)


# ============================================================
# 4. UI 구성
# ============================================================
scene = make_scene("자연어로 만드는 3D 세계 (B안)", width=900, height=550)
scene.append_to_caption("<b>말로 표현하면 AI가 즉시 3D로 시각화한다</b>\n\n")

status = wtext(text="문장을 입력하고 Enter를 누르세요. 예) 빨간 구 5개를 나선으로 배치해줘\n")


def on_submit(w):
    # winput 콜백은 winput 객체를 받는다 → .text로 입력 문장을 꺼낸다
    text_value = w.text
    spec = parse_command_offline(text_value)   # 대회 기본값: 안전한 오프라인 파서
    render_scene(spec)
    status.text = (f"생성 완료: {spec['shape'].__name__} {spec['count']}개, "
                   f"패턴={spec['pattern']}  (입력: \"{text_value}\")\n")


scene.append_to_caption("\n명령 입력 → ")
winput(bind=on_submit, type="string", text="빨간 구 5개를 나선으로 배치해줘")
scene.append_to_caption("  ← 문장 입력 후 Enter\n")

# 이벤트(입력)를 계속 처리하도록 프로그램을 살아있게 유지
while True:
    rate(20)

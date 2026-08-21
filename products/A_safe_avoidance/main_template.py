# main_template.py
"""
⚠️ 보류 상태 파일 (BOILERPLATE ONLY)
당일 이 파일에 시나리오 로직을 채워 넣는다.
위 부품들(vector_helpers, vpython_utils, ui_widgets)을 조립하는 지점.

지금은 실행하지 말 것 — '규정 확인 완료' 및 '아이디어 A안 최종 확정' 신호를 받은 후에만
실제 실행/디버깅한다. 현재는 문법/import 검사만 통과하면 OK.
"""
from vpython import vector, color, rate
from vector_helpers import direction_to, avoid_vector, blend_vectors
from vpython_utils import make_scene, make_agent, make_obstacle, make_floor
from ui_widgets import make_toggle


def run():
    """당일 A안 확정 시 이 함수를 호출해 시뮬레이션을 시작한다."""
    # --- 상태 변수 (당일 시나리오에 맞게 조정) ---
    safe_mode = {"on": True}

    def toggle_safe_mode(checked):
        safe_mode["on"] = checked

    # --- 씬 구성 ---
    make_scene("무해한 AI 시뮬레이터")  # 제목은 최종 아이디어명으로 변경
    make_toggle("무해한 AI: ON (우회함)", "무해한 AI: OFF (돌진함)", toggle_safe_mode, initial=True)

    agent = make_agent(pos=vector(-5, 0, 0))
    obstacle = make_obstacle(pos=vector(0, 0, 0))
    target = make_agent(pos=vector(5, 0, 0), agent_color=color.green, trail=False)

    # --- 애니메이션 루프 ---
    while True:
        rate(60)
        direction = direction_to(agent.pos, target.pos)

        if safe_mode["on"]:
            avoid = avoid_vector(agent.pos, obstacle.pos, threshold=1.5)
            if avoid:
                direction = blend_vectors(direction, avoid, weight=0.6)

        agent.pos += direction * 0.05


# 지금은 자동 실행하지 않는다. 당일 확정 후 아래 주석을 해제한다.
# if __name__ == "__main__":
#     run()

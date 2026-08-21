# parts/dataviz/live_graph.py
"""
VPython 실시간 그래프 부품: 시뮬레이션 결과(대피 시간·탄소량·감염 곡선 등)를
화면에 실시간 선/막대 그래프로 보여준다. VPython 필요.

사용처: 모든 주제의 '결과 정량화' — 심사 어필의 핵심.

사용 예:
    curve = make_line_curve("감염 곡선", "시간", "감염자 수")
    curve.plot(t, infected_count)      # 매 프레임 호출

    bars = make_bars("지역별 만족도", "지역", "만족도")
    bars.data = [[0, 0.8], [1, 0.5], [2, 1.0]]   # 갱신
"""
from vpython import graph, gcurve, gvbars, color


def make_line_curve(title="", xtitle="x", ytitle="y", col=None, width=600, height=250):
    """실시간 꺾은선 그래프. 반환된 곡선에 .plot(x, y)로 점을 추가한다."""
    g = graph(title=title, xtitle=xtitle, ytitle=ytitle,
              width=width, height=height, fast=True)
    return gcurve(graph=g, color=col if col is not None else color.cyan)


def make_bars(title="", xtitle="x", ytitle="y", col=None, delta=0.8, width=600, height=250):
    """실시간 막대 그래프. 반환된 객체의 .data = [[x, y], ...]로 갱신한다."""
    g = graph(title=title, xtitle=xtitle, ytitle=ytitle,
              width=width, height=height, fast=True)
    return gvbars(graph=g, color=col if col is not None else color.orange, delta=delta)

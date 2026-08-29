# DATA_co2_vs_temp/main.py — CO2 농도 vs 지구 기온 상승 추세 비교 (데이터 분석형)
#
# SDG 13(기후). 주최측 예시형: 3D 시뮬이 아니라 '실제 데이터의 추세를 그래프로 비교'.
# 연도별 CO2 농도와 지구 평균기온 이상치를 겹쳐 그려, 두 지표가 나란히 오르는지 본다.
# 데이터: co2_temp.csv (실측 대표값 1960~2020, 오프라인 저장) — 실제 CSV로 교체 가능.
#
# 실행: python main.py

import os
import sys
import csv

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz",
           "input", "gameai", "stats"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import canvas, graph, gcurve, gdots, color, rate, wtext
from stats import pearson, minmax_scale

# ============================================================
# 1. 데이터 읽기 (CSV)
# ============================================================
HERE = os.path.dirname(os.path.abspath(__file__))
years, co2, temp = [], [], []
with open(os.path.join(HERE, "co2_temp.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        years.append(int(row["year"]))
        co2.append(float(row["co2_ppm"]))
        temp.append(float(row["temp_anomaly"]))

co2_norm = minmax_scale(co2)      # 0~100%
temp_norm = minmax_scale(temp)
corr = pearson(co2, temp)         # 상관계수

# ============================================================
# 2. 화면 (그래프 2개 + 설명)
# ============================================================
scene = canvas(width=1, height=1)   # 텍스트 캡션용 최소 캔버스(3D는 안 씀)
scene.append_to_caption("<b>CO2 농도 vs 지구 평균기온 상승 — 실측 대표값(1960~2020) 추세 비교</b>\n")
scene.append_to_caption("① 빨강=CO2, 주황=기온 (같이 오르나?)  ·  ② 파란 점=상관(우상향이면 관계 있음)\n")
info = wtext(text="\n")

g1 = graph(title="① 함께 오르는 추세 (각각 0~100%로 정규화해 겹침)",
           xtitle="연도", ytitle="정규화 수준(%)", width=680, height=280, fast=False)
c_line = gcurve(graph=g1, color=color.red)
t_line = gcurve(graph=g1, color=color.orange)

g2 = graph(title="② CO2 vs 기온 (점들이 우상향 직선이면 강한 상관)",
           xtitle="CO2 농도(ppm)", ytitle="기온 이상치(℃)", width=680, height=280)
dots = gdots(graph=g2, color=color.blue, radius=5)

# ============================================================
# 3. 연도별로 하나씩 그려 넣기 (추세가 그려지는 연출)
# ============================================================
i = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if i < len(years):
        if frame % 8 == 0:
            c_line.plot(years[i], co2_norm[i])
            t_line.plot(years[i], temp_norm[i])
            dots.plot(co2[i], temp[i])
            info.text = f"  {years[i]}년 — CO2 {co2[i]:.0f} ppm,  기온 {temp[i]:+.2f} ℃\n"
            i += 1
            if i == len(years):
                info.text = (
                    f"  ✅ 두 선이 나란히 우상향합니다 → 강한 양의 상관 (상관계수 r = {corr:.2f})\n"
                    f"  ⚠️ 단, 상관관계가 곧 인과는 아닙니다. 배출 급증기와 기온 급등기가 실제로 맞물리는지도 함께 봐야 합니다.\n"
                    f"  → 이 데이터는 '탄소를 줄여야 한다'는 주장의 객관적 근거가 됩니다.\n")

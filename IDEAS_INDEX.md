# 아이디어 인덱스 — "AI와 미래의 공존: 무한한 상상, 무해한 AI"

완성품은 `products/`에, 공통 부품은 `parts/`에 있다. 각 완성품 폴더의 `HANDOFF.md`만 읽으면 바로 이해/착수 가능.

## 구현 상태

| 아이디어 | 폴더 | 컨셉 한 줄 | 난이도 | 상태 |
|---|---|---|---|---|
| A안 | `products/A_safe_avoidance/` | 장애물을 우회하는 무해한 AI | 낮음 | ✅ 완성 |
| D안 | `products/D_trust_visualizer/` | 여러 선택지 중 안전한 것을 고르는 AI 판단 | 낮음 | ✅ 완성 |
| E안 | `products/E_collab_bridge/` | 사람이 목표 지정, AI가 안전 규칙 지키며 다리 건설 | 높음 | ✅ 완성 |
| F안 | `products/F_growth_tree/` | 안전 경계 안에서 자라는 성장 나무 | 중간 | ✅ 완성 |
| B안 | `products/B_nl3d/` | 자연어로 만드는 3D 창작 | 중~상 | ⏳ 검증 대기 |
| 통합안 | `products/combined_adef/` | A+D+E+F를 한 판단 파이프라인으로 연결 | 높음 | ✅ 완성 |

## 선택 가이드
- 시간 부족·안전 → **A안** 또는 **D안**
- 시각적 임팩트 최대 → **F안**
- 공존/협업 메시지 최강 → **E안** / 완성도·통합 → **통합안**

## 공통 실행/테스트 방법
```powershell
# 0) 최초 1회: 설치 (인터넷 필요)
cd C:\Projects\contest
pip install -r requirements.txt

# 각 완성품 실행 (반드시 해당 폴더 안에서)
cd C:\Projects\contest\products\A_safe_avoidance ;  python main.py   # A안
cd C:\Projects\contest\products\D_trust_visualizer ; python main.py  # D안
cd C:\Projects\contest\products\E_collab_bridge ;   python main.py   # E안
cd C:\Projects\contest\products\F_growth_tree ;     python main.py   # F안
cd C:\Projects\contest\products\B_nl3d ;            python main.py   # B안
cd C:\Projects\contest\products\combined_adef ;     python main.py   # 통합안
```
> 각 `main.py`는 맨 위에서 `..\..\parts\<기능>`을 경로에 추가하므로, 그 폴더 안에서 실행하면 부품이 자동 연결된다.

## 공통 전제
- 전부 인터넷 없이 동작 → 대회 전날 Wi-Fi 끄고 각 `python main.py` 1회씩 확인.
- 부품 로직은 `pytest parts/tests/`로 자동 검증됨(47개 통과).

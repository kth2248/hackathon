# 📚 전체 함수 통합 카탈로그 (기능별)

> 지금까지 만든 **모든 재사용 함수**를 기능 종류별로 한곳에 정리. 대회장에서 "이 기능 어디 있지?" 할 때 여기부터 본다.
> 모든 함수는 **`parts/`** 아래 기능별 폴더에 있다(vectors·scene·ui = 예전 hackathon_kit, 나머지 = 알고리즘·AI).
> 완성품(실행 데모)은 **`products/`** 폴더에 따로 모여 있다.
> 순수 = vpython 없이 동작(오프라인·pytest 검증됨) / VPython = 화면 표시용.

---

## 🧮 벡터·수학  `parts/vectors/vector_helpers.py`  (VPython vector)
| 함수 | 하는 일 |
|---|---|
| `direction_to(from, to)` | from→to 단위 방향 벡터 |
| `distance(a, b)` | 두 점 거리 |
| `avoid_vector(agent, obs, threshold)` | 장애물 가까우면 반대 방향, 멀면 None |
| `steer_around(agent, obs, threshold, travel_dir)` | 장애물을 **옆으로 우회**하는 접선 방향 |
| `blend_vectors(v1, v2, weight)` | 두 방향을 비율로 혼합(정규화) |
| `clamp_speed(vel, max_speed)` | 속도 상한 제한 |
> 검증: `pytest parts/tests/test_vector_helpers.py` (20개)

## 🧊 3D 씬·객체  `parts/scene/vpython_utils.py`  (VPython)
| 함수 | 하는 일 |
|---|---|
| `make_scene(title, width, height)` | 캔버스 생성 |
| `make_agent(pos, radius, color, trail, trail_radius)` | 이동 주체 구 |
| `make_obstacle(pos, radius, color)` | 장애물 구 |
| `make_floor(length, width, color, pos, height)` | 바닥 |
| `make_multiple_agents(count, spacing, color)` | 여러 에이전트 일렬 |

### 🧱 격자 렌더링  `parts/scene/grid_render.py`  (VPython, GridWorld와 짝)
| 함수 | 하는 일 |
|---|---|
| `cell_pos(world, cell, y)` | 격자 칸 → 3D 위치 벡터(바닥 x-z평면) |
| `render_floor(world, color, y, thickness)` | 격자 전체 바닥판 |
| `render_obstacles(world, tile, height, color, y)` | 장애물 칸들을 3D 박스로 |

## 🎛️ UI 위젯  `parts/ui/ui_widgets.py`  (VPython)
| 함수 | 하는 일 |
|---|---|
| `make_labeled_slider(min, max, init, on_change, prefix, unit, length, decimals)` | 값 라벨 붙은 슬라이더 |
| `make_toggle(on_text, off_text, on_toggle, initial, checkbox_text)` | 상태 라벨 붙은 체크박스 |

---

## 🗺️ 경로탐색  `parts/pathfinding/astar.py`  (순수)
| 함수 | 하는 일 |
|---|---|
| `astar(start, goal, passable, diagonal)` | A* 최단경로 (칸 리스트) |
| `path_length(path)` | 경로 스텝 수 |

## 🌐 격자 세계  `parts/world/grid.py`  (순수)
| 함수/클래스 | 하는 일 |
|---|---|
| `GridWorld(cols, rows, cell_size, origin)` | 격자 맵 |
| `.passable(cell)` | 지나갈 수 있는 칸? (astar에 넘김) |
| `.block/.unblock(cell)` | 장애물 추가/제거 |
| `.cell_to_world / .world_to_cell` | 격자↔실좌표 변환 |

## 🐦 조향·군집  `parts/steering/steering.py`  (VPython vector)
| 함수 | 하는 일 |
|---|---|
| `seek(pos, target, max_speed)` | 목표로 향함 |
| `arrive(pos, target, max_speed, slow_radius)` | 부드럽게 도착(감속) |
| `separation(pos, neighbors, radius)` | 이웃과 벌어짐(충돌 회피) |
| `alignment(neighbor_vels)` | 무리와 방향 맞춤 |
| `cohesion(pos, neighbors)` | 무리 중심으로 뭉침 |
| `flock(pos, neighbors, vels, sep_radius, weights)` | 위 3개 합친 군집 방향 |

## 🧬 최적화  `parts/optimization/`  (순수)
| 함수 | 파일 | 하는 일 |
|---|---|---|
| `genetic_optimize(create, fitness, mutate, ...)` | genetic.py | 유전알고리즘 최적해 탐색 |
| `proportional_allocate(total, demands)` | allocate.py | 수요 비율대로 배분 |
| `greedy_allocate(total, demands)` | allocate.py | 우선순위 순 배분 |
| `satisfaction(allocated, demand)` | allocate.py | 만족도(0~1) |

## 💬 자연어 파서  `parts/nlp/command_parser.py`  (순수)
| 함수 | 하는 일 |
|---|---|
| `extract_count(text, default, max_count)` | 개수 추출("3개","20그루") |
| `extract_keyword(text, keyword_map, default)` | 키워드→값 매칭 |
| `extract_all_counts(text, keyword_map, max_count)` | "나무 20 태양광 5"→{tree:20,solar:5} |
| `parse(text, fields)` | 여러 필드 한 번에 |

## 🧪 시뮬 모델  `parts/models/`  (순수)
| 함수 | 파일 | 하는 일 |
|---|---|---|
| `infect_step(states, neighbors_of, p_infect, p_recover)` | epidemic.py | 전염병 SIR 한 스텝 |
| `counts(states)` | epidemic.py | (S,I,R) 개수 |
| `reservoir_step(level, inflow, outflow, capacity)` | resource.py | 저수지 수위 갱신 |
| `shortage(demand, supplied)` | resource.py | 부족량 |

## ⚠️ 위험도  `parts/risk/risk.py`  (순수)
| 함수 | 하는 일 |
|---|---|
| `risk_score(pos, obstacles, boundary_radius, avoid_distance)` | 위치 위험도 0~100(연속) |

## 🌀 절차적 배치  `parts/generation/patterns.py`  (순수)
| 함수 | 하는 일 |
|---|---|
| `line_positions(n, spacing, z)` | 일렬 좌표 |
| `spiral_positions(n, growth, angle_step, z_step)` | 나선 좌표 |
| `circle_positions(n, radius)` | 원형 좌표 |
| `grid_positions(n, cols, spacing)` | 격자 좌표 |

## 📈 실시간 그래프  `parts/dataviz/live_graph.py`  (VPython)
| 함수 | 하는 일 |
|---|---|
| `make_line_curve(title, xtitle, ytitle, col)` | 꺾은선 그래프(.plot(x,y)) |
| `make_bars(title, xtitle, ytitle, col, delta)` | 막대 그래프(.data=[[x,y],...]) |

---

## 자동 검증 요약
- `pytest parts/tests/` → 벡터 20 + 알고리즘 27 = **47개 자동 테스트** 통과 (순수 로직 보장)

## 조립 규칙 (다시)
- 필요한 파일이 든 폴더를 `sys.path`에 넣고 import, 또는 파일을 main.py 옆에 복사.
- 모든 함수는 `parts/<기능>`에, 완성품은 `products/`에. `products/`의 main.py는 `../../parts/<기능>`을 경로에 추가해 부품을 불러온다.
- 주제(A~G)별 조합표는 [README.md](README.md) 참고.

# ui_widgets.py
"""
슬라이더/체크박스/라벨을 세트로 묶은 재사용 컴포넌트.
발표 승부처인 '실시간 파라미터 조절'을 위해 어떤 아이디어든 이 패턴을 그대로 씀.
"""
from vpython import slider, checkbox, wtext


def make_labeled_slider(min_val, max_val, init_val, on_change, label_prefix, unit="", length=None, decimals=1):
    """슬라이더 + 값 표시 라벨을 함께 생성.
    on_change(value) 콜백에서 라벨 텍스트를 갱신하도록 래핑.
    length: 슬라이더 픽셀 길이, decimals: 라벨에 표시할 소수점 자리수.
    """
    def _fmt(v):
        # 앞 공백: 슬라이더와 살짝 띄움 / 뒤 \n: 다음 위젯을 새 줄로
        return f"  {label_prefix}: {v:.{decimals}f}{unit}\n"

    def _wrapped(s):
        label.text = _fmt(s.value)
        on_change(s.value)

    slider_kwargs = dict(min=min_val, max=max_val, value=init_val, bind=_wrapped)
    if length is not None:
        slider_kwargs["length"] = length

    # 슬라이더를 '먼저' 만들고, 이름/값 라벨을 그 오른쪽(같은 줄)에 붙인다.
    slider(**slider_kwargs)
    label = wtext(text=_fmt(init_val))
    return label


def make_toggle(label_text_on, label_text_off, on_toggle, initial=True, checkbox_text="토글"):
    """체크박스 + 상태 라벨 세트. A안의 '무해한 AI ON/OFF' 스위치에 바로 사용.
    checkbox_text로 체크박스 옆에 붙는 문구를 지정."""
    label = wtext(text=label_text_on if initial else label_text_off)

    def _wrapped(b):
        label.text = label_text_on if b.checked else label_text_off
        on_toggle(b.checked)

    checkbox(text=checkbox_text, checked=initial, bind=_wrapped)
    return label

# parts/input/keyboard.py
"""
VPython 키보드 입력 추적: 어떤 키가 '지금 눌려 있는지'를 알려준다.
게임에서 플레이어 조작(WASD/화살표)에 사용. 게임 프로그래밍의 '입력 처리' 부품.

사용 예:
    kb = Keyboard(scene)
    dx, dz = kb.axis()          # WASD/화살표 -> (-1..1, -1..1)
    if kb.is_down(' '): ...     # 스페이스
"""


class Keyboard:
    def __init__(self, scene):
        self.pressed = set()
        scene.bind("keydown", self._down)
        scene.bind("keyup", self._up)

    def _down(self, evt):
        self.pressed.add(evt.key)

    def _up(self, evt):
        self.pressed.discard(evt.key)

    def is_down(self, key):
        return key in self.pressed

    def axis(self):
        """WASD 또는 화살표키 -> 이동 방향 성분 (dx, dz), 각 -1/0/1."""
        p = self.pressed
        dx = (1 if ("d" in p or "right" in p) else 0) - (1 if ("a" in p or "left" in p) else 0)
        dz = (1 if ("s" in p or "down" in p) else 0) - (1 if ("w" in p or "up" in p) else 0)
        return (dx, dz)

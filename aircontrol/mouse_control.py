from __future__ import annotations

import time
from dataclasses import dataclass

import pyautogui


@dataclass
class MouseController:
    smoothing: float
    pinch_click_cooldown_seconds: float
    _sx: float | None = None
    _sy: float | None = None
    _last_click_time: float = 0.0

    def update_cursor(self, x_norm: float, y_norm: float) -> None:
        screen_w, screen_h = pyautogui.size()
        tx = max(0.0, min(1.0, x_norm)) * screen_w
        ty = max(0.0, min(1.0, y_norm)) * screen_h

        if self._sx is None or self._sy is None:
            self._sx, self._sy = tx, ty
        else:
            a = max(0.0, min(1.0, self.smoothing))
            self._sx = (a * self._sx) + ((1.0 - a) * tx)
            self._sy = (a * self._sy) + ((1.0 - a) * ty)

        pyautogui.moveTo(self._sx, self._sy, duration=0)

    def try_click(self) -> bool:
        now = time.time()
        if (now - self._last_click_time) < self.pinch_click_cooldown_seconds:
            return False
        pyautogui.click()
        self._last_click_time = now
        return True

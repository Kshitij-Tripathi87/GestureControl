from __future__ import annotations

import time
from dataclasses import dataclass, field

import pyautogui

from .gestures import (
    GESTURE_FIST,
    GESTURE_INDEX_UP,
    GESTURE_OPEN_PALM,
    GESTURE_PINKY_UP,
    GESTURE_THUMB_UP,
    GESTURE_THUMB_DOWN,
    GESTURE_THREE_FINGERS,
)


@dataclass
class ActionExecutor:
    
    cooldown_seconds: float
    _last_action_time: float = field(default=0.0, init=False)
    _last_action_name: str = field(default="NO_ACTION", init=False)

    def _cooldown_elapsed(self) -> bool:
        return (time.monotonic() - self._last_action_time) >= self.cooldown_seconds

    def try_execute(self, stable_gesture: str) -> str:
        action_name = "NO_ACTION"

        if not self._cooldown_elapsed():
            return action_name

        if stable_gesture == GESTURE_OPEN_PALM:
            pyautogui.press("space")
            action_name = "KEY_SPACE"
        elif stable_gesture == GESTURE_FIST:
            pyautogui.press("left")
            action_name = "KEY_LEFT"
        elif stable_gesture == GESTURE_THUMB_UP:
            pyautogui.press("right")
            action_name = "KEY_RIGHT"
        elif stable_gesture == GESTURE_INDEX_UP:
            pyautogui.press("volumeup")
            action_name = "VOLUME_UP"
        elif stable_gesture == GESTURE_PINKY_UP:
            pyautogui.press("volumedown")
            action_name = "VOLUME_DOWN"
        elif stable_gesture == GESTURE_THREE_FINGERS:
            pyautogui.press("brightnessup")
            action_name = "BRIGHTNESS_UP"
        elif stable_gesture == GESTURE_THUMB_DOWN:
            pyautogui.press("brightnessdown")
            action_name = "BRIGHTNESS_DOWN"

        if action_name != "NO_ACTION":
            self._last_action_time = time.monotonic()
            self._last_action_name = action_name

        return action_name

    @property
    def last_action_name(self) -> str:
        return self._last_action_name

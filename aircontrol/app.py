from __future__ import annotations

import time

import cv2
import mediapipe as mp
import pyautogui

from .config import AirControlConfig
from .controls import ActionExecutor
from .gestures import (
    GESTURE_NONE,
    GESTURE_PINCH,
    GESTURE_SHAKA,
    GESTURE_V_SIGN,
    GestureStabilizer,
    classify_gesture,
)
from .mouse_control import MouseController


def _draw_overlay(
    frame,
    raw_gesture: str,
    stable_gesture: str,
    action: str,
    *,
    armed: bool,
    mode: str,
) -> None:
    h, w = frame.shape[:2]
    panel_h = 160
    cv2.rectangle(frame, (0, 0), (w, panel_h), (0, 0, 0), -1)
    cv2.putText(
        frame,
        f"Raw: {raw_gesture}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        frame,
        f"Stable: {stable_gesture}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )
    cv2.putText(
        frame,
        f"Action: {action}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        f"Mode: {mode}    Armed: {'ON' if armed else 'OFF'}",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 200, 0),
        2,
    )
    cv2.putText(
        frame,
        "V_SIGN toggles ARM | SHAKA toggles MOUSE | Q quits",
        (20, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        2,
    )


def run() -> None:
    config = AirControlConfig()
    pyautogui.FAILSAFE = False

    cap = cv2.VideoCapture(config.camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.camera_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.camera_height)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check camera permissions/device index.")

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    stabilizer = GestureStabilizer(
        history_size=config.prediction_history_size,
        min_stable_votes=config.min_stable_votes,
    )
    executor = ActionExecutor(cooldown_seconds=config.action_cooldown_seconds)
    mouse = MouseController(
        smoothing=config.mouse_smoothing,
        pinch_click_cooldown_seconds=config.pinch_click_cooldown_seconds,
    )

    armed = False
    mode = "PRESENTATION"
    last_toggle_time = 0.0

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=config.min_detection_confidence,
        min_tracking_confidence=config.min_tracking_confidence,
    ) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            raw_gesture = GESTURE_NONE
            stable_gesture = GESTURE_NONE
            action = "NO_ACTION"

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                )
                raw_gesture = classify_gesture(hand_landmarks.landmark)
                stable_gesture = stabilizer.update(raw_gesture)

                now = time.time()
                can_toggle = (now - last_toggle_time) >= config.toggle_cooldown_seconds

                if stable_gesture == GESTURE_V_SIGN and can_toggle:
                    armed = not armed
                    last_toggle_time = now
                    action = f"ARM_{'ON' if armed else 'OFF'}"
                elif stable_gesture == GESTURE_SHAKA and can_toggle:
                    mode = "MOUSE" if mode == "PRESENTATION" else "PRESENTATION"
                    last_toggle_time = now
                    action = f"MODE_{mode}"
                else:
                    if mode == "MOUSE":
                        if config.mouse_move_enabled:
                            idx_tip = hand_landmarks.landmark[8]
                            mouse.update_cursor(idx_tip.x, idx_tip.y)
                        if stable_gesture == GESTURE_PINCH and mouse.try_click():
                            action = "MOUSE_CLICK"
                    else:
                        if armed and stable_gesture != GESTURE_NONE:
                            action = executor.try_execute(stable_gesture)

            _draw_overlay(frame, raw_gesture, stable_gesture, action, armed=armed, mode=mode)
            cv2.imshow("AirControl - Gesture PC Control", frame)

            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

    cap.release()
    cv2.destroyAllWindows()

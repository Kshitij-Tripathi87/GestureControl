

from dataclasses import dataclass


@dataclass(frozen=True)
class AirControlConfig:
    camera_index: int = 0
    camera_width: int = 1280
    camera_height: int = 720

    prediction_history_size: int = 7
    min_stable_votes: int = 5

    action_cooldown_seconds: float = 1.25

    toggle_cooldown_seconds: float = 1.0

    mouse_smoothing: float = 0.35
    mouse_move_enabled: bool = True
    pinch_click_cooldown_seconds: float = 0.6

    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.7

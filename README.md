# AirControl

AirControl is a local, webcam-based computer vision project that lets you control presentation and desktop actions with hand gestures. It is built as a practical capstone MVP using OpenCV, MediaPipe Hands, and PyAutoGUI.

## What The Project Does

- Opens your webcam and tracks one hand in real time
- Recognizes gestures using rule-based landmark logic (no external gesture model files)
- Stabilizes predictions across frames to reduce false triggers
- Uses cooldown timing so actions do not repeat too quickly
- Executes mapped keyboard/system commands while showing live status on screen

## Quick Start / How To Operate

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

How to use it:
- Keep your hand visible and well lit in front of the camera
- Keep the app you want to control (for example PowerPoint) in focus
- Hold a gesture briefly so it becomes stable
- Press `Q` in the OpenCV window to quit

## Configuration

Edit `aircontrol/config.py` to tune behavior:

- `prediction_history_size`: number of recent predictions used for smoothing
- `min_stable_votes`: votes needed before a gesture is accepted
- `action_cooldown_seconds`: delay between action triggers
- `camera_index`, `camera_width`, `camera_height`: webcam source and resolution
- `min_detection_confidence`, `min_tracking_confidence`: hand detection/tracking sensitivity

## Gesture Mapping

| Gesture | Action |
|---|---|
| `V_SIGN` | Toggle **Armed ON/OFF** |
| `SHAKA` (thumb + pinky) | Toggle **Mouse Mode / Presentation Mode** |
| `PINCH` (thumb + index) | **Mouse click** (Mouse Mode) |
| `OPEN_PALM` | `Space` (Presentation Mode, Armed) |
| `FIST` | `Left Arrow` (Presentation Mode, Armed) |
| `THUMB_UP` | `Right Arrow` (Presentation Mode, Armed) |
| `INDEX_UP` | `Volume Up` |
| `PINKY_UP` | `Volume Down` |
| `THREE_FINGERS`| `Brightness Up` |
| `THUMB_DOWN` | `Brightness Down` |

To change what each gesture does, edit `aircontrol/controls.py`.

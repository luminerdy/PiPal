# PiPal

A lightweight interactive character developed and run directly on Raspberry Pi 5.

## Current prototype

Two eyes blink and gently idle fullscreen on HDMI. The Logitech C920 can drive
pupil position using a local OpenCV frontal-face detector. Good lighting and a
reasonably close, forward-facing person work best. Full-body detection, speech,
and an AI agent are not implemented. The USB speaker arrives later.

No camera frames or audio are recorded or uploaded. No automatic startup is set.
See docs/HARDWARE.md for actual verification and outstanding checks.

## Run

From a terminal in the Pi desktop:

```sh
cd ~/PiPal
./run.sh
```

Escape closes the eyes; Ctrl+C stops a foreground launch. Close any existing
instance before opening the camera again. Optional modes:

```sh
./run.sh --demo                 # Eyes without camera access
./run.sh --windowed             # Resizable development window
./run.sh --no-mirror-x          # Opposite horizontal mapping for other placements
./run.sh --seconds 30           # Timed check
./run.sh --help
```

For SSH, first verify the active desktop account and Wayland socket.
The tested socket was `wayland-0`; adapt this example to your session:

```sh
cd ~/PiPal
XDG_RUNTIME_DIR="/run/user/$(id -u)" WAYLAND_DISPLAY=wayland-0 SDL_VIDEODRIVER=wayland ./run.sh
```

Recheck these session values after account, OS, or desktop changes. Run as the desktop account, not root. The launcher does not configure a desktop session for you.

The camera defaults to one discovered C920 video-index0 stable device link. If
there are several cameras, inspect them and select one with `--camera PATH`.
Horizontal mirroring is enabled by default after the user tested this placement.
`--capture-width`, `--capture-height`, and `--detect-hz` adjust performance. Start
with the tested 640x480 capture and 10 Hz maximum detection rate.

## Dependencies

This Pi uses Debian system Python packages, including its existing Pygame.
No pip installation or virtual environment is required for this prototype:

```sh
sudo apt-get install --no-install-recommends python3-opencv opencv-data python3-pygame
```

The face cascade comes from opencv-data. Nothing is downloaded at runtime.
requirements.txt records the OS package choices; it is intentionally not a pip
installer. See HARDWARE.md for installed versions and validation.

## Check and continue

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
./run.sh --demo --windowed --seconds 5
```

Tests cover direction/clamping, time-based smoothing, and target selection.
Hardware tests must also verify movement, target loss, blinking, and quitting.
A valid camera with no face produces idle motion. Camera failure exits with an
error; reconnect and restart manually. This is not yet an unattended service.

To continue locally with Codex:

```sh
cd ~/PiPal
codex
```

Suggested prompt:

> Read AGENTS.md and docs/, especially the validation and open checks. Inspect
> the current implementation and Pi hardware before changing it. Complete any
> outstanding milestone 1 checks with me, then propose the smallest useful next
> improvement. The USB speaker is not connected yet. Keep this lightweight.

app.py owns the loop, tracking.py captures/detects, gaze.py handles motion math,
and eyes.py draws the character. Ignored data/ is for local operational logs and
checks of rendered display output, never camera recordings.

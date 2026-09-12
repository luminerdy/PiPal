# Raspberry Pi 5 hardware findings

Inspected over SSH on 2026-09-11. Observed unless marked pending.

| Item | Finding |
| --- | --- |
| OS | Debian 13 (trixie), release 13.6 |
| Architecture / Python | aarch64 / 3.13.5 |
| Memory / disk at inspection | 7.9 GiB RAM / about 20 GiB free in home filesystem |
| Initial temperature / throttling | 59.3 C / vcgencmd get_throttled: 0x0 |
| Camera | Logitech C920, USB 046d:082d |
| Capture link | `/dev/v4l/by-id/*C920*video-index0` (serial omitted; discover locally) |
| Capture link target at inspection | /dev/video0; index1 points to /dev/video1 and is not selected |
| Advertised formats | YUYV, H264, MJPG; includes 640x480 at 30 FPS |
| Permissions | Desktop account in video, render, audio groups |
| Desktop | labwc / Wayland, local session 1 |
| Runtime / socket | Per-user runtime directory / wayland-0 |
| HDMI | HDMI-A-2, Samsung S27C500, 1920x1080 at 60 Hz, scale 1 |
| Pygame | python3-pygame 2.6.1-1+b2, previously installed |
| OpenCV / cascade data | python3-opencv and opencv-data 4.10.0+dfsg-5 installed |
| Audio | PipeWire 1.4.2 / WirePlumber; HDMI output, volume 0.40; playback untested |
| Microphone | C920 Analog Stereo enumerated; no capture test |
| USB speaker | Not present; user expects it tomorrow |

Methods: OS/Python queries, lsusb, v4l2-ctl device/format enumeration, loginctl,
wlr-randr, wpctl, free, df, package queries, vcgencmd. Power supply and cooling
arrangement have not been physically inspected.

## Validation

- Four hardware-independent gaze tests passed on the Pi.
- 3-second windowed demo: 960x540, 30.3 FPS, clean exit.
- 8-second fullscreen demo: 1920x1080 on Wayland, 30.2 FPS, clean exit.
- Persistent demo: HDMI-A-2 output visually inspected; user confirmed seeing eyes.
- Brief demo sample: roughly 23% CPU (one-core convention), 139 MB resident memory.
- C920 capture passed twice: 45 frames each at actual 640x480 MJPG, negotiated
  30 FPS; capture plus detection on every frame measured 24.7 and 20.4 FPS.
- Camera reopened cleanly between tests.
- Windowed tracking detected faces in both quit tests. SIGINT/Ctrl+C and injected
  Escape event both exited successfully, with camera reopening afterwards.
- SIGINT initially interrupted a blocking read and produced a spurious camera
  error; fixed by respecting the stop signal when capture returns an error.
- Fullscreen camera tracking initially started at 20:53 local time. The user
  reported reversed horizontal motion; horizontal mirroring is now the default.
  Tracking restarted after the correction for a fresh stability check.
- User confirmed corrected left/right AND up/down tracking on the physical display.
- Live logs show tracking -> idle -> tracking -> idle, confirming target loss
  and reacquisition at the software level. The user confirmed motion direction.
- Missing-camera test returned exit code 1 with an actionable message.
- Five-minute stability check PASSED after the direction correction: process alive
  at 306 seconds, no runtime errors, 23.8-30.0 rendering FPS, 8.0-8.9 detection Hz
  across the first 31 ten-second reporting intervals, 207 face-positive passes.
- Resident memory held at 262560 kB during monitoring; final CPU sample 54.2%
  (one-core convention). Monitored temperatures 70.8-74.7 C; every throttle query
  returned 0x0. These readings describe this run, not a guarantee in all rooms.
- Remaining field checks: multiple-person target steadiness and longer-term
  robustness under changing lighting/range. Milestone 1 prototype is working;
  full field acceptance remains open. Audio milestones are not started.

## Current handoff

The fullscreen tracker is left running under the desktop account. Escape closes it. From a desktop
terminal use `cd ~/PiPal` then `./run.sh` to restart. SSH session settings and all
options are in README.md. Operational logs are in ignored `data/tracking.log`;
the stability samples are in `data/stability.log`. No auto-start service exists.
A temporary HDMI screenshot was used to verify the eyes rendering; camera frames
were never saved or transferred. No account secrets were copied into this project.

Recheck device/session choices after hardware, desktop, or OS changes.

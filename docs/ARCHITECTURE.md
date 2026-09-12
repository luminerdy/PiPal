# Minimal architecture

```text
C920 -> OpenCV capture -> frontal-face cascade -> target -> smoothed gaze
                                                            |
                                                            v
                                                 Pygame eyes on HDMI
```

One Python process owns one loop. It requests 640x480 capture at 30 FPS, detects
on a 320-pixel-wide grayscale image at up to 10 Hz, and renders at up to 30 FPS.
Actual rates are measured on the Pi. Capture and detection are synchronous;
measure before adding threads.

- app.py: options, events, loop, operational logs, and cleanup.
- tracking.py: V4L2 capture and packaged OpenCV frontal-face cascade.
- gaze.py: target selection, normalization, and time-based smoothing.
- eyes.py: two eyes, bounded iris travel, blinking, and gentle idle motion.

Select the largest face initially, then prefer a nearby previously selected face
while present. This simple heuristic needs a multiple-person field check. No
identity is retained. After 0.8 seconds without a target, return to idle gaze.
Horizontal mapping is mirrored by default for the tested camera placement;
--no-mirror-x reverses it. Only frontal faces are supported initially; person
detection is a later option.

Escape/window close, SIGINT (Ctrl+C), SIGTERM, and an optional time limit stop the
loop and release resources. A driver stuck in a blocking capture read may delay
exit; unattended recovery is not implemented. Missing devices produce errors.

Camera pixels never reach the eyes renderer and are never recorded. Logs contain
operational state, rates, and aggregate detection counts. Demo mode does not open
the camera. Only Pygame's display module initializes; microphone and speaker stay
unused.

Later add speaker, microphone, TTS/STT, then an AI agent behind text-in/text-out.
Those operations must avoid freezing the eyes. Choose concurrency when needed.
No database, web UI, broker, container, service manager, or provider is selected.

References:
- https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html
- https://www.pygame.org/docs/ref/display.html

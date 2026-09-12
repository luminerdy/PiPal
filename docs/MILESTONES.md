# Milestones

Milestone 0 inspection is recorded in HARDWARE.md. Milestone 1 is implemented
and under validation; display, camera capture/detection, and quit checks passed.
The user confirmed the eyes are visible and both tracking directions are correct.
Live tracking passed a five-minute stability run and loss/reacquisition appears
in its logs. Multiple-person and extended lighting/range field checks remain;
see HARDWARE.md for evidence and limitations.
Do not mark it complete until the outstanding hardware checks pass. Milestones
2-5 are unimplemented. The USB speaker arrives later. Keep each step small.

## 0 — Inspect the Pi

Complete `HARDWARE.md`, identify a usable camera capture interface and graphical
session, and propose the smallest detection/rendering stack.

Acceptance: findings distinguish verified facts from unknowns; required packages
and system changes are explained before installation.

## 1 — Tracking eyes on HDMI

First verify camera capture, then render two eyes in a window, then connect
face/person location to pupil position and enable fullscreen. Include smoothing,
occasional blinking, target-loss idle behavior, and an easy quit path.

Acceptance on the Pi:

- The C920 supplies live frames; a person moving left/right and up/down causes
  the pupils to move in the intended direction without leaving the eye shapes.
- HDMI fullscreen shows both eyes correctly at the detected display size.
- Losing the target returns to idle; reacquiring it resumes tracking. Multiple
  visible targets follow a documented selection rule without excessive jumping.
- A five-minute run stays responsive. Record observed rendering/detection rates,
  CPU/memory use, and any thermal or stability problems; tune based on results.
- Escape and Ctrl+C exit cleanly, and a subsequent run can reopen the camera.
- Missing camera/display errors are understandable. No sensor data is recorded
  or uploaded. A person at the display confirms appearance and motion.

Face tracking alone satisfies this milestone if reliable in the intended setup.
Add person detection only if needed for range or robustness.

## 2 — USB speaker output

Discover and select the USB speaker. Play a short local sound at a user-confirmed
comfortable volume while the eyes continue to animate.

Acceptance: sound comes from the intended speaker; unavailable output fails
gracefully; visual tracking still works.

## 3 — Microphone input

Inspect available sources and confirm the intended microphone, potentially the
C920 microphone if present and usable. Begin with a local input-level indicator.

Acceptance: the selected input responds to speech, listening state is visible,
and capture can be stopped. Recording is off by default.

## 4 — TTS and STT

Choose local or cloud speech components based on measured Pi performance, desired
latency, and the user's data-sharing preferences. Start with explicit push-to-talk
or another deliberate trigger; prevent speaker output from retriggering input.

Acceptance: a short utterance becomes text and a supplied text response plays
through the USB speaker without freezing the eyes. Timeouts and errors leave the
character usable. Any network data flow and credentials are documented.

## 5 — AI agent

Connect recognized text to a small conversational agent and speak its responses.
Define the character's behavior, provider configuration, conversation retention,
and permitted actions explicitly. Start with conversation only.

Acceptance: one complete voice exchange works; the user can stop speech; network
or provider failure does not break the eyes; secrets are kept outside source
control. Add memory, tools, and automatic startup only when specifically needed.

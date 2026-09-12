# Working on PiPal

## Scope

Build a simple interactive character on the Raspberry Pi 5 where this project
runs. The first milestone is C920 face/person tracking driving animated eyes
fullscreen over HDMI. See `docs/MILESTONES.md` for later work.

## Inspect before choosing

- Read the README and docs. Inspect the real OS, architecture, Python version,
  available memory, camera interfaces, and graphical session before selecting
  libraries. Record verified findings in `docs/HARDWARE.md`.
- Do not assume `/dev/video0`, a camera index, an audio card number, an HDMI
  connector name, display resolution, or a particular desktop/window system.
  A camera can expose more than one interface; verify an actual capture stream.
- Distinguish command output, inference, and observations confirmed by the user.
  Never claim a visual or audio check passed solely because a process started.

## Make the smallest working increment

- Keep one Python process and a straightforward loop initially. Add modules only
  when they hold real behavior; no plugin framework or speculative abstractions.
- Verify camera capture, then eyes rendering, then connect them. Prefer a face
  detector first if suitable; do not require two detection pipelines at launch.
- Keep capture resolution and detection frequency adjustable after measuring on
  the Pi. Avoid downloading large models before explaining the need.
- Put dependencies in `requirements.txt` once chosen. Document OS dependencies
  separately and record versions actually tested. Use a project virtual
  environment when appropriate; do not replace the system Python.
- Keep device selection configurable when implemented and document discovery.
  Do not commit a developer machine's device paths as universal defaults.
- Release camera/display resources on exit. Provide Escape and Ctrl+C exit paths,
  a no-target idle state, and useful errors when devices cannot be opened.
- Add focused tests only where they help, such as coordinate mapping and gaze
  smoothing. Pair them with actual camera/display checks on the Pi.

## Boundaries

- Project edits and read-only inspection are expected. Obtain approval before
  system package installation, changing permissions/groups, system configuration,
  boot behavior, or enabling services unless the user already authorized it.
- Start manually in the Pi's graphical session. Do not assume an SSH session can
  open a fullscreen window on the attached HDMI display.
- Process camera frames in memory by default. Do not record images or audio,
  identify people, or upload sensor data without explicit user direction.
- Keep credentials out of source control. Later cloud services must have a
  documented configuration and data flow before being connected.

## Handoff

Keep docs aligned with implemented behavior. Report what changed, commands used
to run it, checks actually performed, and unresolved hardware limitations. Mark
a milestone complete only after its acceptance checks have been verified.

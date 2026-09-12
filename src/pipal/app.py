"""One process, one capture/detect/render loop for the first PiPal prototype."""
import argparse
import logging
import math
import os
import signal
import time

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

from .gaze import choose_face, normalized_center, smooth


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be a positive finite number')
    return number


def main():
    parser = argparse.ArgumentParser(description='PiPal: camera-driven eyes. Escape or Ctrl+C to quit.')
    parser.add_argument('--camera', help='Explicit capture device path; default discovers one C920')
    parser.add_argument('--windowed', action='store_true', help='Use a resizable 960x540 window')
    parser.add_argument('--demo', action='store_true', help='Animated eyes without opening a camera')
    parser.add_argument('--mirror-x', action=argparse.BooleanOptionalAction, default=True,
                        help='Mirror horizontal gaze (default); use --no-mirror-x for opposite placement')
    parser.add_argument('--detect-hz', type=positive, default=10, help='Maximum detection rate (default: 10)')
    parser.add_argument('--seconds', type=positive, help='Stop automatically after this many seconds')
    parser.add_argument('--capture-width', type=int, default=640)
    parser.add_argument('--capture-height', type=int, default=480)
    args = parser.parse_args()
    if min(args.capture_width, args.capture_height) <= 0:
        parser.error('capture dimensions must be positive')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    try:
        import pygame
        from .eyes import Eyes, idle_gaze
        from .tracking import Tracker
    except ImportError as exc:
        logging.error('Missing dependency: %s. See README.md.', exc)
        return 1
    tracker = None
    running = True

    def stop(signum, frame):
        nonlocal running
        running = False

    old_handlers = {sig: signal.signal(sig, stop) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        if not args.demo:
            tracker = Tracker(args.camera, args.capture_width, args.capture_height)
            logging.info('Camera: %s (frames stay in memory)', tracker.camera)
        if not (os.environ.get('WAYLAND_DISPLAY') or os.environ.get('DISPLAY')
                or os.environ.get('SDL_VIDEODRIVER') == 'dummy'):
            raise RuntimeError('No graphical session. Run ./run.sh in the Pi desktop terminal; see README.md for SSH.')
        pygame.display.init()  # Do not initialize audio or open the microphone.
        screen = pygame.display.set_mode((960, 540) if args.windowed else (0, 0),
                                         pygame.RESIZABLE if args.windowed else pygame.FULLSCREEN)
        pygame.display.set_caption('PiPal - Escape to quit')
        pygame.mouse.set_visible(args.windowed)
        logging.info('Display: %s, %s, fullscreen=%s', pygame.display.get_driver(), screen.get_size(), not args.windowed)
        eyes, clock = Eyes(), pygame.time.Clock()
        started = last_tick = last_stats = time.monotonic()
        next_detect, last_seen = started, -math.inf
        gaze = target = (0.0, 0.0)
        selected = None
        frames = detections = hits = 0
        total_frames = total_detections = total_hits = 0
        while running:
            now = time.monotonic()
            if args.seconds and now - started >= args.seconds:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            if not running:
                break
            if tracker:
                try:
                    frame = tracker.read()
                except RuntimeError:
                    # SIGINT/SIGTERM can interrupt a blocking V4L2 read.
                    if not running:
                        break
                    raise
                if now >= next_detect:
                    faces, (width, height) = tracker.detect(frame)
                    selected = choose_face(faces, selected if now - last_seen < 0.8 else None)
                    detections += 1
                    if selected is not None:
                        target = normalized_center(selected, width, height, args.mirror_x)
                        last_seen = now
                        hits += 1
                    next_detect = now + 1 / args.detect_hz
                del frame
            if now - last_seen > 0.8:
                target = idle_gaze(now - started)
            gaze = smooth(gaze, target, min(now - last_tick, 0.25))
            last_tick = now
            eyes.draw(screen, gaze, now - started)
            pygame.display.flip()
            frames += 1
            if now - last_stats >= 10:
                interval = now - last_stats
                logging.info('render=%.1f fps detect=%.1f Hz face_hits=%d state=%s',
                             frames / interval, detections / interval, hits,
                             'tracking' if now - last_seen <= 0.8 else 'idle')
                total_frames += frames
                total_detections += detections
                total_hits += hits
                frames = detections = hits = 0
                last_stats = now
            clock.tick(30)
        elapsed = max(0.001, time.monotonic() - started)
        logging.info('Stopped: %.1fs, render=%.1f fps detect=%.1f Hz face_hits=%d', elapsed,
                     (total_frames + frames) / elapsed, (total_detections + detections) / elapsed, total_hits + hits)
        return 0
    except (RuntimeError, pygame.error) as exc:
        logging.error('%s', exc)
        return 1
    except Exception:
        logging.exception('Unexpected failure')
        return 1
    finally:
        if tracker:
            tracker.close()
        pygame.quit()
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)

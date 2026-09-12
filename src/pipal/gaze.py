"""Small, hardware-independent gaze math."""
import math


def normalized_center(box, width, height, mirror_x=False):
    x, y, w, h = box
    nx = max(-1.0, min(1.0, 2 * (x + w / 2) / width - 1))
    ny = max(-1.0, min(1.0, 2 * (y + h / 2) / height - 1))
    return (-nx if mirror_x else nx), ny


def smooth(current, target, dt, response=7.0):
    alpha = 1 - math.exp(-response * max(0, dt))
    return tuple(a + (b - a) * alpha for a, b in zip(current, target))


def choose_face(faces, previous=None):
    """Keep a nearby target; otherwise select the largest visible face."""
    if len(faces) == 0:
        return None
    if previous is not None:
        px, py, pw, ph = previous
        close = [f for f in faces if math.hypot(
            f[0] + f[2] / 2 - px - pw / 2,
            f[1] + f[3] / 2 - py - ph / 2,
        ) < max(pw, ph)]
        if close:
            return min(close, key=lambda f: math.hypot(
                f[0] + f[2] / 2 - px - pw / 2,
                f[1] + f[3] / 2 - py - ph / 2,
            ))
    return max(faces, key=lambda f: f[2] * f[3])

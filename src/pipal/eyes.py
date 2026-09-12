"""Draw two eyes; camera pixels never reach this renderer."""
import math
import random

import pygame

BACKGROUND = (7, 13, 23)


class Eyes:
    def __init__(self):
        self.next_blink = 2.0

    def draw(self, screen, gaze, elapsed):
        screen.fill(BACKGROUND)
        width, height = screen.get_size()
        scale = min(width / 960, height / 540)
        openness = 1.0
        if elapsed >= self.next_blink:
            phase = (elapsed - self.next_blink) / 0.20
            if phase >= 1:
                self.next_blink = elapsed + random.uniform(2.5, 5.0)
            else:
                openness = max(0.025, abs(2 * phase - 1))
        for offset in (-205, 205):
            cx, cy = width / 2 + offset * scale, height / 2
            ew, eh = 310 * scale, 340 * scale
            eye = pygame.Rect(0, 0, round(ew), round(eh))
            eye.center = round(cx), round(cy)
            pygame.draw.ellipse(screen, (221, 238, 240), eye)
            # Bounded travel keeps the full iris inside the sclera.
            px = round(cx + gaze[0] * 58 * scale)
            py = round(cy + gaze[1] * 66 * scale)
            pygame.draw.circle(screen, (41, 168, 181), (px, py), max(1, round(72 * scale)))
            pygame.draw.circle(screen, (15, 68, 86), (px, py), max(1, round(58 * scale)))
            pygame.draw.circle(screen, (5, 14, 25), (px, py), max(1, round(43 * scale)))
            pygame.draw.circle(screen, (241, 255, 255),
                               (px - round(18 * scale), py - round(22 * scale)), max(1, round(12 * scale)))
            pygame.draw.circle(screen, (104, 200, 209),
                               (px + round(18 * scale), py + round(20 * scale)), max(1, round(5 * scale)))
            cover = round(eh * (1 - openness) / 2)
            if cover:
                pygame.draw.rect(screen, BACKGROUND, (eye.x, eye.y, eye.width, cover))
                pygame.draw.rect(screen, BACKGROUND, (eye.x, eye.bottom - cover, eye.width, cover))


def idle_gaze(elapsed):
    return 0.12 * math.sin(elapsed * 0.5), 0.07 * math.sin(elapsed * 0.37)

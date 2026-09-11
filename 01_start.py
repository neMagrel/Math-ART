"""Canonical classroom starter for the Math Art Generator masterclass."""

import colorsys
import math

import pygame


WIDTH, HEIGHT = 1000, 720
FPS = 60
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BACKGROUND = (5, 6, 14)

# Parameters students will use and personalize later.
a = 3
b = 4
speed = 1.0
particle_count = 18
trail_fade = 18
point_radius = 4
line_width = 2
radius_x = 360
radius_y = 250

time_value = 0.0
hue_shift = 0.0


def hsv_color(hue: float, saturation=0.85, value=1.0):
    """Convert an HSV hue into an RGB color for Pygame."""
    red, green, blue = colorsys.hsv_to_rgb(hue % 1.0, saturation, value)
    return int(red * 255), int(green * 255), int(blue * 255)


pygame.init()
pygame.display.set_caption("Math Art Generator - classroom starter")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.fill(BACKGROUND)

fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_surface.fill((*BACKGROUND, trail_fade))

previous_points = [None] * particle_count
running = True

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    hue_shift = (hue_shift + dt * 0.08 * speed) % 1.0

    # Old pixels fade gradually; students only connect their drawing to this.
    trail_surface.blit(fade_surface, (0, 0))

    if len(previous_points) != particle_count:
        previous_points = [None] * particle_count

    # ============================================================
    # КОД УЧЕНИКА
    # ============================================================

    # Здесь код будет появляться по этапам мастер-класса.

    # ============================================================
    # КОНЕЦ КОДА УЧЕНИКА
    # ============================================================

    screen.blit(trail_surface, (0, 0))
    pygame.display.flip()

pygame.quit()

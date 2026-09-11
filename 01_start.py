"""Canonical classroom starter for the Math Art Generator masterclass."""

import math

import pygame


WIDTH, HEIGHT = 1000, 720
FPS = 60
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BACKGROUND = (5, 6, 14)


pygame.init()
pygame.display.set_caption("Math Art Generator - classroom starter")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BACKGROUND)

    # ============================================================
    # КОД УЧЕНИКА
    # ============================================================

    # Здесь код будет появляться по этапам мастер-класса.

    # ============================================================
    # КОНЕЦ КОДА УЧЕНИКА
    # ============================================================

    pygame.display.flip()

pygame.quit()

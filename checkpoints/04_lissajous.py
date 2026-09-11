"""Canonical classroom starter for the Math Art Generator masterclass."""

import colorsys
import math
import random
from pathlib import Path

import pygame

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None


WIDTH, HEIGHT = 1000, 720
FPS = 60
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BACKGROUND = (5, 6, 14)

PROJECT_ROOT = Path(__file__).resolve().parent
if PROJECT_ROOT.name == "checkpoints":
    PROJECT_ROOT = PROJECT_ROOT.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

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
show_help = True

# GIF recording is a teacher-owned bonus feature.
recording = False
recorded_frames = []
MAX_GIF_FRAMES = 160
GIF_CAPTURE_EVERY = 3
frame_counter = 0


def hsv_color(hue: float, saturation=0.85, value=1.0):
    """Convert an HSV hue into an RGB color for Pygame."""
    red, green, blue = colorsys.hsv_to_rgb(hue % 1.0, saturation, value)
    return int(red * 255), int(green * 255), int(blue * 255)


def save_png(surface):
    """Save the current clean art surface as a PNG."""
    path = OUTPUT_DIR / "math_art_wallpaper.png"
    pygame.image.save(surface, path)
    print(f"PNG saved: {path}")


def save_gif(frames):
    """Save captured surfaces as GIF when Pillow is available."""
    if not PIL_AVAILABLE:
        print("GIF is unavailable: install Pillow before class. PNG still works.")
        return

    if not frames:
        print("GIF was not saved: there are no captured frames.")
        return

    path = OUTPUT_DIR / "math_art_animation.gif"
    images = []

    for frame_surface in frames:
        raw = pygame.image.tostring(frame_surface, "RGB")
        images.append(Image.frombytes("RGB", frame_surface.get_size(), raw))

    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=50,
        loop=0,
        optimize=False,
    )
    print(f"GIF saved: {path}")


def randomize():
    """Choose a new combination of parameters for later exploration."""
    global a, b, particle_count, speed, point_radius

    a = random.randint(2, 9)
    b = random.randint(2, 9)
    if a == b:
        b = b % 9 + 1

    particle_count = random.randint(8, 28)
    speed = random.choice([0.6, 0.8, 1.0, 1.2, 1.5])
    point_radius = random.randint(2, 6)


def draw_interface(screen, font, small_font):
    """Draw status and ready-made controls for the classroom."""
    title = font.render(
        f"Math Art Generator   a={a}   b={b}   "
        f"speed={speed:.1f}   particles={particle_count}",
        True,
        (235, 235, 245),
    )
    screen.blit(title, (20, 16))

    if recording:
        text = small_font.render(
            f"REC GIF: {len(recorded_frames)}/{MAX_GIF_FRAMES}",
            True,
            (255, 120, 120),
        )
        screen.blit(text, (20, 50))

    if show_help:
        lines = [
            "LEFT / RIGHT  - change a",
            "UP / DOWN     - change b",
            "W / S         - speed",
            "+ / -         - particles",
            "SPACE         - random pattern",
            "R             - clear trail",
            "P             - save PNG",
            "G             - start / stop GIF",
            "H             - hide help",
            "ESC           - exit",
        ]

        panel = pygame.Surface((330, 265), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 135))
        screen.blit(panel, (20, HEIGHT - 285))

        y = HEIGHT - 270
        for line in lines:
            text = small_font.render(line, True, (210, 215, 230))
            screen.blit(text, (35, y))
            y += 24


pygame.init()
pygame.display.set_caption("Math Art Generator - classroom starter")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.fill(BACKGROUND)

fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_surface.fill((*BACKGROUND, trail_fade))

previous_points = [None] * particle_count
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    frame_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_LEFT:
                a = max(1, a - 1)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_RIGHT:
                a = min(12, a + 1)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_DOWN:
                b = max(1, b - 1)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_UP:
                b = min(12, b + 1)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_w:
                speed = min(3.0, speed + 0.1)

            elif event.key == pygame.K_s:
                speed = max(0.1, speed - 0.1)

            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                particle_count = min(60, particle_count + 1)
                previous_points = [None] * particle_count

            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                particle_count = max(1, particle_count - 1)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_SPACE:
                randomize()
                trail_surface.fill(BACKGROUND)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_r:
                trail_surface.fill(BACKGROUND)
                previous_points = [None] * particle_count

            elif event.key == pygame.K_h:
                show_help = not show_help

            elif event.key == pygame.K_p:
                save_png(trail_surface.copy())

            elif event.key == pygame.K_g:
                if recording:
                    recording = False
                    save_gif(recorded_frames)
                    recorded_frames = []
                elif PIL_AVAILABLE:
                    recording = True
                    recorded_frames = []
                    print("GIF recording started...")
                else:
                    save_gif([])

    hue_shift = (hue_shift + dt * 0.08 * speed) % 1.0

    # Old pixels fade gradually; students only connect their drawing to this.
    trail_surface.blit(fade_surface, (0, 0))

    if len(previous_points) != particle_count:
        previous_points = [None] * particle_count

    # ============================================================
    # КОД УЧЕНИКА
    # ============================================================

    time_value += dt * speed

    x = CENTER_X + math.sin(a * time_value) * radius_x
    y = CENTER_Y + math.sin(b * time_value) * radius_y

    pygame.draw.circle(
        trail_surface,
        (255, 255, 255),
        (int(x), int(y)),
        point_radius,
    )

    # ============================================================
    # КОНЕЦ КОДА УЧЕНИКА
    # ============================================================

    screen.blit(trail_surface, (0, 0))
    draw_interface(screen, font, small_font)
    pygame.display.flip()

    if recording and frame_counter % GIF_CAPTURE_EVERY == 0:
        recorded_frames.append(trail_surface.copy())

        if len(recorded_frames) >= MAX_GIF_FRAMES:
            recording = False
            save_gif(recorded_frames)
            recorded_frames = []

pygame.quit()

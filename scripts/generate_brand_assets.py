from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"
FONT_DIR = ROOT / "assets" / "fonts"

PAPER = "#f3eee4"
INK = "#121017"
INK_SOFT = "#34303c"
COPPER = "#b96433"
STEEL = "#8898ab"
SAND = "#d8cdb8"


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
  return ImageFont.truetype(str(FONT_DIR / name), size=size)


def make_canvas(width: int, height: int, transparent: bool = False) -> Image.Image:
  if transparent:
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))
  image = Image.new("RGBA", (width, height), PAPER)
  draw = ImageDraw.Draw(image)
  for y in range(0, height, 16):
    alpha = 10 if (y // 16) % 3 == 0 else 5
    draw.line((0, y, width, y), fill=(18, 16, 23, alpha), width=1)
  noise = Image.effect_noise((width, height), 10).convert("L").filter(ImageFilter.GaussianBlur(0.5))
  grain = Image.new("RGBA", (width, height), (0, 0, 0, 0))
  grain.putalpha(noise.point(lambda value: 18 if value > 132 else 0))
  return Image.alpha_composite(image, grain)


def draw_orbital_system(draw: ImageDraw.ImageDraw, center: tuple[int, int], scale: float, opacity: int = 255) -> None:
  cx, cy = center
  ring_colors = [
    (18, 16, 23, opacity),
    (185, 100, 51, int(opacity * 0.92)),
    (136, 152, 171, int(opacity * 0.82)),
    (18, 16, 23, int(opacity * 0.5))
  ]
  radii = [170, 235, 302, 352]
  widths = [6, 4, 3, 2]
  for index, radius in enumerate(radii):
    box = (
      int(cx - radius * scale),
      int(cy - radius * scale),
      int(cx + radius * scale),
      int(cy + radius * scale)
    )
    draw.arc(box, start=8 + (index * 13), end=315 - (index * 11), fill=ring_colors[index], width=max(1, int(widths[index] * scale)))
  for angle in (18, 72, 129, 188, 242, 307):
    radians = math.radians(angle)
    outer = 372 * scale
    inner = 42 * scale
    x1 = cx + math.cos(radians) * inner
    y1 = cy + math.sin(radians) * inner
    x2 = cx + math.cos(radians) * outer
    y2 = cy + math.sin(radians) * outer
    draw.line((x1, y1, x2, y2), fill=(18, 16, 23, int(opacity * 0.16)), width=max(1, int(2 * scale)))
  for dx, dy, radius, color in (
    (-145, -72, 16, COPPER),
    (196, 122, 10, STEEL),
    (38, -208, 12, INK),
    (-238, 164, 8, COPPER)
  ):
    x = cx + int(dx * scale)
    y = cy + int(dy * scale)
    r = max(2, int(radius * scale))
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
  draw.ellipse(
    (cx - int(52 * scale), cy - int(52 * scale), cx + int(52 * scale), cy + int(52 * scale)),
    outline=(18, 16, 23, int(opacity * 0.9)),
    width=max(1, int(5 * scale))
  )
  draw.line((cx - int(18 * scale), cy, cx + int(18 * scale), cy), fill=(18, 16, 23, opacity), width=max(1, int(3 * scale)))
  draw.line((cx, cy - int(18 * scale), cx, cy + int(18 * scale)), fill=(18, 16, 23, opacity), width=max(1, int(3 * scale)))


def draw_measure_labels(draw: ImageDraw.ImageDraw, width: int, height: int, big: bool = True) -> None:
  mono = load_font("GeistMono-Regular.ttf", 28 if big else 17)
  mono_bold = load_font("GeistMono-Bold.ttf", 24 if big else 14)
  labels = [
    ("FRONTIER MODEL", (72, 70)),
    ("01 / ORBITAL LEDGER", (72, height - 96)),
    ("CODING", (width - 250, 92)),
    ("AGENTS", (width - 250, 128)),
    ("1M CONTEXT", (width - 250, 164))
  ]
  for text, (x, y) in labels:
    draw.text((x, y), text, font=mono, fill=INK_SOFT)
  draw.rectangle((72, 108, 220, 114), fill=SAND)
  draw.rectangle((width - 336, 78, width - 286, 84), fill=COPPER)
  draw.text((72, 124), "CLAUDE OPUS 4.7", font=mono_bold, fill=INK)


def generate_logo_mark() -> None:
  image = make_canvas(1200, 1200, transparent=True)
  draw = ImageDraw.Draw(image)
  draw_orbital_system(draw, (600, 600), 1.3)
  image.save(BRAND_DIR / "logo-mark.png")


def generate_logo_wordmark() -> None:
  image = make_canvas(1800, 560, transparent=True)
  draw = ImageDraw.Draw(image)
  draw_orbital_system(draw, (260, 280), 0.56)

  serif = load_font("Gloock-Regular.ttf", 132)
  sans = load_font("InstrumentSans-Regular.ttf", 38)
  mono = load_font("GeistMono-Regular.ttf", 24)

  draw.text((470, 156), "Claude Opus", font=serif, fill=INK)
  draw.text((472, 304), "4.7", font=serif, fill=COPPER)
  draw.line((470, 118, 1540, 118), fill=SAND, width=4)
  draw.text((474, 96), "INDEPENDENT EDITORIAL REVIEW", font=mono, fill=INK_SOFT)
  draw.text((476, 404), "Coding / Agents / Long-context knowledge work", font=sans, fill=INK_SOFT)
  image.save(BRAND_DIR / "logo-wordmark.png")


def generate_square_icon(filename: str, size: int) -> None:
  image = make_canvas(size, size)
  draw = ImageDraw.Draw(image)
  margin = int(size * 0.1)
  draw.rounded_rectangle((margin, margin, size - margin, size - margin), radius=int(size * 0.06), outline=SAND, width=max(2, size // 120))
  draw_orbital_system(draw, (size // 2, size // 2), size / 900, opacity=255)
  mono = load_font("GeistMono-Bold.ttf", max(18, size // 10))
  draw.text((margin + size * 0.03, size - margin - size * 0.14), "4.7", font=mono, fill=COPPER)
  image.save(BRAND_DIR / filename)


def generate_social_card() -> None:
  width, height = 1600, 900
  image = make_canvas(width, height)
  draw = ImageDraw.Draw(image)
  draw.rectangle((58, 58, width - 58, height - 58), outline=SAND, width=2)
  draw.rectangle((92, 92, width - 92, height - 92), outline=(18, 16, 23, 28), width=1)
  draw_orbital_system(draw, (1110, 462), 1.05)
  draw_measure_labels(draw, width, height)

  serif_big = load_font("Gloock-Regular.ttf", 132)
  serif_small = load_font("Gloock-Regular.ttf", 80)
  sans = load_font("InstrumentSans-Regular.ttf", 42)
  mono = load_font("GeistMono-Regular.ttf", 22)

  draw.text((72, 244), "Claude", font=serif_big, fill=INK)
  draw.text((72, 376), "Opus 4.7", font=serif_big, fill=COPPER)
  draw.text((72, 558), "Reviewing the premium Claude tier for coding,\nAI agents, and high-context knowledge work.", font=sans, fill=INK_SOFT, spacing=10)
  draw.text((72, 730), "Updated April 18, 2026", font=mono, fill=INK_SOFT)
  draw.text((72, 770), "claudeopus47.lol", font=serif_small, fill=INK)
  image.save(BRAND_DIR / "social-card.png")


def main() -> None:
  BRAND_DIR.mkdir(parents=True, exist_ok=True)
  generate_logo_mark()
  generate_logo_wordmark()
  generate_square_icon("favicon.png", 512)
  generate_square_icon("apple-touch-icon.png", 180)
  generate_social_card()


if __name__ == "__main__":
  main()

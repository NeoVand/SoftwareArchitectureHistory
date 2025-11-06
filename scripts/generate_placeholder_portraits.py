"""Generate stylized placeholder portrait SVGs for architecture figures."""
from __future__ import annotations

import os
from typing import Iterable, Sequence, Tuple

FIGURES: Sequence[Tuple[str, str, Sequence[str], Tuple[int, int, int]]] = (
    ("mary-shaw", "Mary Shaw", ("Software architecture co-author", "Championed quality attributes"), (88, 35, 175)),
    ("david-garlan", "David Garlan", ("Architectural styles researcher", "CMU Software Engineering Institute"), (16, 120, 80)),
    ("kent-beck", "Kent Beck", ("Extreme Programming creator", "Popularized Test-Driven Development"), (200, 70, 20)),
    ("martin-fowler", "Martin Fowler", ("Thoughtworks chief scientist", "Chronicled enterprise patterns"), (24, 96, 160)),
    ("ward-cunningham", "Ward Cunningham", ("Invented the wiki", "Agile collaboration icon"), (160, 40, 80)),
    ("jeff-sutherland", "Jeff Sutherland", ("Scrum co-creator", "Brought lean thinking to software"), (18, 120, 60)),
    ("alistair-cockburn", "Alistair Cockburn", ("Agile Manifesto signer", "Documented the Crystal methods"), (210, 50, 50)),
    ("ken-schwaber", "Ken Schwaber", ("Scrum co-founder", "Drove global Agile adoption"), (40, 60, 160)),
    ("arie-van-bennekum", "Arie van Bennekum", ("Agile facilitator", "Guided large-scale change"), (110, 70, 160)),
    ("mike-beedle", "Mike Beedle", ("Enterprise Scrum champion", "Early Agile Manifesto author"), (220, 120, 30)),
    ("charity-majors", "Charity Majors", ("Observability advocate", "Co-founded Honeycomb"), (20, 24, 40)),
    ("adrian-cockcroft", "Adrian Cockcroft", ("Netflix cloud architect", "Evangelized microservices"), (8, 110, 160)),
    ("werner-vogels", "Werner Vogels", ("AWS chief technologist", "You build it, you run it"), (210, 170, 20)),
    ("dhh", "David Heinemeier Hansson", ("Created Ruby on Rails", "Promoted convention over configuration"), (180, 28, 110)),
)

WIDTH = 640
HEIGHT = 360
MARGIN_X = 48
TITLE_Y = 92
LINE_GAP = 30


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#" + "".join(f"{channel:02x}" for channel in rgb)


def lerp_color(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    return tuple(
        max(0, min(255, int(channel * (1 - factor) + 15 * factor))) for channel in color
    )


def format_lines(lines: Iterable[str]) -> Sequence[str]:
    return [line.strip() for line in lines if line.strip()]


def portrait_svg(slug: str, name: str, lines: Sequence[str], base_color: Tuple[int, int, int]) -> str:
    gradient_id = f"grad-{slug}"
    accent_id = f"accent-{slug}"
    start = to_hex(lerp_color(base_color, 0.0))
    end = to_hex(lerp_color(base_color, 0.6))
    accent = to_hex(lerp_color(base_color, 0.8))
    summary = format_lines(lines)
    body_lines = [f"• {text}" for text in summary]

    text_elements = [
        f"  <text x=\"{MARGIN_X}\" y=\"{TITLE_Y}\" font-size=\"40\" font-family=\"'Segoe UI', Arial, sans-serif\" fill=\"#f8fafc\" font-weight=\"700\">{name}</text>",
        f"  <text x=\"{MARGIN_X}\" y=\"{TITLE_Y + LINE_GAP}\" font-size=\"22\" font-family=\"'Segoe UI', Arial, sans-serif\" fill=\"#e2e8f0\">{summary[0] if summary else ''}</text>",
    ]
    for index, line in enumerate(body_lines[1:], start=2):
        text_elements.append(
            f"  <text x=\"{MARGIN_X}\" y=\"{TITLE_Y + index * LINE_GAP}\" font-size=\"20\" font-family=\"'Segoe UI', Arial, sans-serif\" fill=\"#e2e8f0\">{line}</text>"
        )

    outline = f"""
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{WIDTH}\" height=\"{HEIGHT}\" viewBox=\"0 0 {WIDTH} {HEIGHT}\">
  <defs>
    <linearGradient id=\"{gradient_id}\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"{start}\" stop-opacity=\"0.95\" />
      <stop offset=\"100%\" stop-color=\"{end}\" stop-opacity=\"0.98\" />
    </linearGradient>
    <linearGradient id=\"{accent_id}\" x1=\"0%\" y1=\"0%\" x2=\"0%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"{accent}\" stop-opacity=\"0.75\" />
      <stop offset=\"100%\" stop-color=\"{accent}\" stop-opacity=\"0.05\" />
    </linearGradient>
  </defs>
  <rect width=\"{WIDTH}\" height=\"{HEIGHT}\" rx=\"32\" fill=\"url(#{gradient_id})\" />
  <circle cx=\"{WIDTH * 0.22:.0f}\" cy=\"{HEIGHT * 0.36:.0f}\" r=\"72\" fill=\"#f4f4f5\" opacity=\"0.92\" />
  <path d=\"M {WIDTH * 0.11:.0f} {HEIGHT * 0.58:.0f} q {WIDTH * 0.11:.0f} {HEIGHT * 0.14:.0f} {WIDTH * 0.22:.0f} 0\"
        fill=\"url(#{accent_id})\" opacity=\"0.8\" />
  {os.linesep.join(text_elements)}
</svg>
""".strip()
    return outline


def write_portrait(path: str, svg_body: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(svg_body)
        handle.write("\n")


def main() -> None:
    output_dir = os.path.join("images", "portraits")
    ensure_output_dir(output_dir)
    for slug, name, lines, base_color in FIGURES:
        svg = portrait_svg(slug, name, lines, base_color)
        write_portrait(os.path.join(output_dir, f"{slug}.svg"), svg)
    print(f"Generated {len(FIGURES)} SVG portraits in {output_dir}")


if __name__ == "__main__":
    main()

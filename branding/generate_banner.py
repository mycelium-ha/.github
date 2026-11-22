"""Generate the profile banner (light and dark) from the avatar mark.

Usage: python branding/generate_banner.py branding   (needs cairosvg and the Noto Sans font)
"""
import sys
from pathlib import Path
import cairosvg

out_dir = Path(sys.argv[1])

MARK = """
  <g transform="translate({x} {y}) scale({s}) translate(-512 -495)">
    <path d="M512 200 L 784 430 L 784 800 L 240 800 L 240 430 Z"
          fill="url(#mark)" stroke="url(#mark)" stroke-width="64" stroke-linejoin="round"/>
    <g clip-path="url(#house-clip)">
      <g fill="none" stroke="#0F2C26" stroke-width="24" stroke-linecap="round">
        <path d="M424 476 C 494 474, 566 500, 618 534"/>
        <path d="M618 534 C 590 596, 552 646, 494 676"/>
        <path d="M494 676 C 452 612, 428 546, 424 476"/>
        <path d="M424 476 C 396 404, 364 344, 312 280"/>
        <path d="M424 476 C 350 486, 270 508, 150 544"/>
        <path d="M618 534 C 650 444, 684 372, 740 300"/>
        <path d="M618 534 C 706 586, 770 638, 880 700"/>
        <path d="M494 676 C 500 740, 496 800, 486 900"/>
      </g>
    </g>
    <g fill="#0F2C26">
      <circle cx="424" cy="476" r="38"/>
      <circle cx="618" cy="534" r="38"/>
      <circle cx="494" cy="676" r="46"/>
    </g>
    <circle cx="494" cy="676" r="25" fill="#F6B94B"/>
  </g>"""

THEMES = {
    "dark": dict(bg1="#11332C", bg2="#0A1F1B", title="#EAFBF3", tag="#9CCFBC"),
    "light": dict(bg1="#F3FBF7", bg2="#E2F4EB", title="#0F2C26", tag="#3D6A5C"),
}

for name, t in THEMES.items():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>
    <linearGradient id="mark" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="#A6F6D1"/><stop offset="1" stop-color="#33BC96"/>
    </linearGradient>
    <clipPath id="house-clip">
      <path d="M512 158.1 L 816 415.2 L 816 832 L 208 832 L 208 415.2 Z"/>
    </clipPath>
  </defs>
  <rect width="1280" height="320" rx="24" fill="url(#bg)"/>

  {MARK.format(x=176, y=160, s=0.29)}
  <text x="312" y="160" font-family="Noto Sans" font-weight="700" font-size="64"
        letter-spacing="-1" fill="{t['title']}">Mycelium HA</text>
  <text x="314" y="214" font-family="Noto Sans" font-size="30" fill="{t['tag']}">Integrations for Home Assistant. Local first, reliable by design.</text>
</svg>"""
    (out_dir / f"banner-{name}.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out_dir / f"banner-{name}.png"),
                     output_width=2560, output_height=640)
    print("wrote", name)

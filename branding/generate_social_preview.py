"""Generate a GitHub social preview image (1280 x 640) for an integration.

Usage:
    python branding/generate_social_preview.py <out.png> "<Title>" "<Subtitle>"

Needs cairosvg and the Noto Sans font. Upload the PNG under the repository's
Settings > General > Social preview (GitHub has no API for it).
"""

import sys
from xml.sax.saxutils import escape

import cairosvg

out, title, subtitle = sys.argv[1:4]

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
      <circle cx="424" cy="476" r="38"/><circle cx="618" cy="534" r="38"/><circle cx="494" cy="676" r="46"/>
    </g>
    <circle cx="494" cy="676" r="25" fill="#F6B94B"/>
  </g>"""

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#11332C"/><stop offset="1" stop-color="#0A1F1B"/>
    </linearGradient>
    <linearGradient id="mark" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="#A6F6D1"/><stop offset="1" stop-color="#33BC96"/>
    </linearGradient>
    <clipPath id="house-clip">
      <path d="M512 158.1 L 816 415.2 L 816 832 L 208 832 L 208 415.2 Z"/>
    </clipPath>
  </defs>
  <rect width="1280" height="640" fill="url(#bg)"/>
  {MARK.format(x=1080, y=300, s=0.34)}
  <text x="96" y="268" font-family="Noto Sans" font-weight="700" font-size="76"
        letter-spacing="-1" fill="#EAFBF3">{escape(title)}</text>
  <text x="98" y="336" font-family="Noto Sans" font-size="30" fill="#9CCFBC">{escape(subtitle)}</text>
  <rect x="98" y="420" width="56" height="4" rx="2" fill="#F6B94B"/>
  <text x="98" y="476" font-family="Noto Sans" font-weight="700" font-size="28" fill="#EAFBF3">Mycelium HA</text>
  <text x="98" y="514" font-family="Noto Sans" font-size="24" fill="#9CCFBC">Integrations for Home Assistant</text>
</svg>"""

cairosvg.svg2png(bytestring=svg.encode(), write_to=out, output_width=1280, output_height=640)
print("wrote", out)

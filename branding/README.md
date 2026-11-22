# Branding

The mycelium-ha mark: a solid house divided into organic cells by a hyphal network. The amber node is the hub where everything connects.

| File | Use |
| --- | --- |
| [`avatar.svg`](avatar.svg) | Source (1024 × 1024 vector) |
| [`avatar.png`](avatar.png) | Organization avatar (1024 × 1024) |
| [`banner-light.png`](banner-light.png), [`banner-dark.png`](banner-dark.png) | Profile README header (2560 × 640), shown by color scheme |
| [`generate_banner.py`](generate_banner.py) | Regenerates both banners and their SVG sources |

## Colors

| Role | Hex |
| --- | --- |
| Background (top → bottom) | `#11332C` → `#0A1F1B` |
| Mark (gradient) | `#A6F6D1` → `#33BC96` |
| Network lines | `#0F2C26` |
| Hub accent | `#F6B94B` |

## Usage

- Place the mark on the dark background or the light banner background (`#F3FBF7` → `#E2F4EB`). Don't recolor it, rotate it, or add effects.
- Typeface: Noto Sans (Bold for the name, Regular for text).
- Say "Mycelium HA" in text; `mycelium-ha` only for handles and URLs.
- Integrations ship their own brand images (`custom_components/<domain>/brand/`) showing the product they integrate, not this mark.
- Re-export the PNG from the SVG at 1024 × 1024 after changes.

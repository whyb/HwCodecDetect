"""
GUI Theme Constants (Fluent Design + macOS inspired dark theme).
Shared between gui.py and color_table.py to avoid circular imports.
"""
import sys

# ─── Color Palette ───────────────────────────────────────────────────────────
BG_ROOT       = "#1b1d23"     # deepest background
BG_SIDEBAR    = "#20222a"     # sidebar
BG_SURFACE    = "#272a33"     # card / surface
BG_ELEVATED   = "#2f3240"     # elevated surface
BG_INPUT      = "#353845"     # input fields
BG_HOVER      = "#3a3e50"     # hover state
BORDER        = "#3a3d48"     # subtle border
BORDER_LIGHT  = "#4a4e5c"     # lighter border
TEXT_PRIMARY   = "#ecedf2"    # primary text
TEXT_SECONDARY = "#9197a8"    # secondary text
TEXT_DIM       = "#626878"    # dim text
ACCENT        = "#6b8aff"     # accent blue (softer)
ACCENT_HOVER  = "#839dff"     # accent hover
ACCENT_SUBTLE = "#2a3158"     # accent subtle bg
GREEN         = "#4ade80"     # success green
GREEN_BG      = "#14291a"     # green background
GREEN_BORDER  = "#22543d"     # green border
RED           = "#f87171"     # error red
RED_BG        = "#2d1518"     # red background
RED_BORDER    = "#7f1d1d"     # red border
ORANGE        = "#fbbf24"     # warning orange
ORANGE_BG     = "#2d2510"     # orange background
ORANGE_BORDER = "#785815"     # orange border
PURPLE        = "#c084fc"     # purple accent
CYAN          = "#67e8f9"     # cyan accent
PROGRESS_BG   = "#2a2d38"     # progress bar background
PROGRESS_FG   = "#6b8aff"     # progress bar fill
SEPARATOR     = "#2a2d38"     # separator
NAV_ACTIVE    = "#2f3240"     # active nav bg
NAV_HOVER     = "#2a2d38"     # nav hover bg
BADGE_BG      = "#6b8aff22"   # badge background

# ─── Font Families ───────────────────────────────────────────────────────────
FAMILY = "Segoe UI"
FAMILY_MONO = "Cascadia Code"
if sys.platform != "win32":
    FAMILY = "Helvetica Neue"
    FAMILY_MONO = "Menlo"

"""
Finishing calculator: areas and material quantities for one room.
Pure geometry. No database, no AI, no prices.
"""

import math

# Typical waste allowance for cutting tiles and paper. Verify on site.
DEFAULT_ALLOWANCE = 0.10


def room_areas(length, width, height, openings=None):
    """
    length, width, height in meters.
    openings: list of (width, height) tuples for doors and windows.
    """
    openings = openings or []
    floor = length * width
    ceiling = length * width
    wall_gross = 2 * (length + width) * height
    openings_area = sum(w * h for w, h in openings)
    wall_net = wall_gross - openings_area
    return {
        "floor_m2": round(floor, 2),
        "ceiling_m2": round(ceiling, 2),
        "wall_gross_m2": round(wall_gross, 2),
        "openings_m2": round(openings_area, 2),
        "wall_net_m2": round(wall_net, 2),
        "formula_wall": f"2 x ({length} + {width}) x {height} - openings {round(openings_area, 2)}",
    }


def with_allowance(area_m2, allowance=DEFAULT_ALLOWANCE):
    """Add waste allowance, e.g. 10%."""
    return round(area_m2 * (1 + allowance), 2)


def packs_needed(area_m2, pack_area_m2):
    """Round up to whole packs. You cannot buy 0.07 of a box."""
    return math.ceil(round(area_m2 / pack_area_m2, 6))


def paint_liters(area_m2, coats, m2_per_liter):
    """Liters = area x coats / coverage per liter (from the product datasheet)."""
    return round(area_m2 * coats / m2_per_liter, 2)


def tile_count(area_m2, tile_w_cm, tile_h_cm, allowance=DEFAULT_ALLOWANCE):
    """Number of tiles for an area. Tile size is entered in centimeters, any rectangle."""
    if tile_w_cm <= 0 or tile_h_cm <= 0:
        raise ValueError("Tile size must be positive")
    tile_area = (tile_w_cm / 100) * (tile_h_cm / 100)
    needed = area_m2 * (1 + allowance)
    # round(...,6) avoids 11.0000001 turning into 12 tiles
    tiles = math.ceil(round(needed / tile_area, 6))
    return {
        "tiles": tiles,
        "tile_area_m2": round(tile_area, 4),
        "formula": f"{round(needed, 2)} m2 / {round(tile_area, 4)} m2 per tile, rounded up",
    }


def tile_packs(tiles, pieces_per_pack):
    """Whole packs needed. Pieces per pack comes from the product card."""
    if pieces_per_pack <= 0:
        raise ValueError("Pieces per pack must be positive")
    return math.ceil(round(tiles / pieces_per_pack, 6))

"""
Hand-checked tests for finishing_calculator. Numbers are worked out on paper.
"""

from finishing_calculator import room_areas, with_allowance, packs_needed, paint_liters


def test_room_example_walls():
    # Room 3 x 4 m, height 2.7 m, door 0.8 x 2.0, window 1.2 x 1.4
    # Gross walls: 2 x (3 + 4) x 2.7 = 37.8
    # Openings: 1.6 + 1.68 = 3.28
    # Net walls: 37.8 - 3.28 = 34.52
    r = room_areas(3, 4, 2.7, openings=[(0.8, 2.0), (1.2, 1.4)])
    assert r["floor_m2"] == 12.0
    assert r["ceiling_m2"] == 12.0
    assert r["wall_gross_m2"] == 37.8
    assert r["openings_m2"] == 3.28
    assert r["wall_net_m2"] == 34.52


def test_allowance_on_walls():
    # 34.52 x 1.1 = 37.972 -> 37.97
    assert with_allowance(34.52, 0.10) == 37.97


def test_tiles_round_up_to_whole_boxes():
    # 7.3 m2 needed, box covers 1.62 m2 -> 4.51 boxes -> 5 boxes
    assert packs_needed(7.3, 1.62) == 5


def test_paint_liters():
    # 10 m2, 2 coats, 10 m2 per liter -> 2 liters
    assert paint_liters(10, 2, 10) == 2.0


def _close(a, b):
    # Compare with a small tolerance, because of rounding to 2 decimals
    return abs(a - b) < 0.01


def test_room_A_small_kitchen():
    # 2.5 x 3.0 m, height 2.6, door 0.7 x 2.0
    r = room_areas(2.5, 3.0, 2.6, openings=[(0.7, 2.0)])
    assert _close(r["floor_m2"], 7.5)
    assert _close(r["ceiling_m2"], 7.5)
    assert _close(r["wall_gross_m2"], 28.6)
    assert _close(r["openings_m2"], 1.4)
    assert _close(r["wall_net_m2"], 27.2)


def test_room_B_two_windows():
    # 4.0 x 5.0 m, height 2.8, two windows 1.5 x 1.4
    r = room_areas(4.0, 5.0, 2.8, openings=[(1.5, 1.4), (1.5, 1.4)])
    assert _close(r["floor_m2"], 20.0)
    assert _close(r["ceiling_m2"], 20.0)
    assert _close(r["wall_gross_m2"], 50.4)
    assert _close(r["openings_m2"], 4.2)
    assert _close(r["wall_net_m2"], 46.2)


def test_room_C_balcony_door():
    # 3.5 x 3.5 m, height 2.7, balcony door 1.6 x 2.2
    r = room_areas(3.5, 3.5, 2.7, openings=[(1.6, 2.2)])
    assert _close(r["floor_m2"], 12.25)
    assert _close(r["wall_gross_m2"], 37.8)
    assert _close(r["openings_m2"], 3.52)
    assert _close(r["wall_net_m2"], 34.28)


def test_room_D_allowance_on_walls():
    # 3.0 x 3.0 m, height 2.5, no openings
    r = room_areas(3.0, 3.0, 2.5)
    assert _close(r["wall_gross_m2"], 30.0)
    assert _close(with_allowance(r["wall_gross_m2"]), 33.0)


from finishing_calculator import tile_count, tile_packs


def test_tile_30x30_ten_square_meters():
    # 10 m2 + 10% = 11 m2; 11 / 0.09 = 122.2 -> 123 tiles
    r = tile_count(10, 30, 30)
    assert r["tiles"] == 123


def test_tile_30x30_packs_of_18():
    # 123 tiles / 18 per pack = 6.8 -> 7 packs (Atem 30x30 pack is 18 pcs)
    assert tile_packs(123, 18) == 7


def test_tile_60x60():
    # 11 / 0.36 = 30.6 -> 31 tiles
    assert tile_count(10, 60, 60)["tiles"] == 31


def test_tile_90x90():
    # 11 / 0.81 = 13.58 -> 14 tiles
    assert tile_count(10, 90, 90)["tiles"] == 14


def test_tile_100x100_exact_no_extra_tile():
    # 11 / 1.0 = 11.0 exactly -> 11 tiles, not 12
    assert tile_count(10, 100, 100)["tiles"] == 11


def test_tile_rectangle_30x60():
    # 11 / 0.18 = 61.1 -> 62 tiles
    assert tile_count(10, 30, 60)["tiles"] == 62


def test_tile_rejects_zero_size():
    import pytest
    with pytest.raises(ValueError):
        tile_count(10, 0, 30)

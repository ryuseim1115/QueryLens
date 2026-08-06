from api.services.query_structure.depth_analyzer import get_query_block_depth


def test_empty_ranges_is_depth_zero():
    assert get_query_block_depth((0, 20), []) == 0


def test_single_range_is_depth_zero():
    assert get_query_block_depth((0, 20), [(0, 20)]) == 0


def test_two_non_overlapping_ranges_both_zero():
    ranges = [(0, 10), (15, 25)]
    assert get_query_block_depth((0, 10), ranges) == 0
    assert get_query_block_depth((15, 25), ranges) == 0


def test_nested_outer_zero_inner_one():
    # (0, 50) contains (10, 30)
    ranges = [(0, 50), (10, 30)]
    assert get_query_block_depth((0, 50), ranges) == 0
    assert get_query_block_depth((10, 30), ranges) == 1


def test_doubly_nested_three_levels():
    # (0, 100) > (10, 80) > (20, 60)
    ranges = [(0, 100), (10, 80), (20, 60)]
    assert get_query_block_depth((0, 100), ranges) == 0
    assert get_query_block_depth((10, 80), ranges) == 1
    assert get_query_block_depth((20, 60), ranges) == 2


def test_two_siblings_inside_one_parent():
    # (0, 100) contains both (10, 40) and (50, 90)
    ranges = [(0, 100), (10, 40), (50, 90)]
    assert get_query_block_depth((0, 100), ranges) == 0
    assert get_query_block_depth((10, 40), ranges) == 1
    assert get_query_block_depth((50, 90), ranges) == 1

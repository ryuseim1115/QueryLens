from api.services.query_structure.depth_analyzer import get_query_block_depths


def test_empty_returns_empty():
    assert get_query_block_depths([]) == []


def test_single_range_is_depth_zero():
    assert get_query_block_depths([(0, 20)]) == [0]


def test_two_non_overlapping_ranges_both_zero():
    depths = get_query_block_depths([(0, 10), (15, 25)])
    assert depths == [0, 0]


def test_nested_outer_zero_inner_one():
    # (0, 50) contains (10, 30)
    depths = get_query_block_depths([(0, 50), (10, 30)])
    assert depths[0] == 0
    assert depths[1] == 1


def test_doubly_nested_three_levels():
    # (0, 100) > (10, 80) > (20, 60)
    depths = get_query_block_depths([(0, 100), (10, 80), (20, 60)])
    assert depths[0] == 0
    assert depths[1] == 1
    assert depths[2] == 2


def test_two_siblings_inside_one_parent():
    # (0, 100) contains both (10, 40) and (50, 90)
    depths = get_query_block_depths([(0, 100), (10, 40), (50, 90)])
    assert depths[0] == 0
    assert depths[1] == 1
    assert depths[2] == 1

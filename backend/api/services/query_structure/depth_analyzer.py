def get_query_block_depth(
    target: tuple[int, int],
    ranges: list[tuple[int, int]],
) -> int:
    # target を完全に含む range（surrounding）の数をカウントすることでネスト深さを算出する
    target_start, target_end = target
    depth = 0
    for surrounding_start, surrounding_end in ranges:
        # target が surrounding の内側に完全に収まる場合、depth を加算
        if target_start > surrounding_start and target_end < surrounding_end:
            depth += 1
    return depth

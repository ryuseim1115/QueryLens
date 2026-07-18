def get_query_block_depths(ranges: list[tuple[int, int]]) -> list[int]:
    # 各範囲について、自身を完全に含む範囲の数をカウントすることでネスト深さを算出する
    depths = []
    for target_start, target_end in ranges:
        depth = 0
        for search_start, search_end in ranges:
            # target が search の内側に完全に収まる場合、depth を加算
            if target_start > search_start and target_end < search_end:
                depth += 1
        depths.append(depth)
    return depths

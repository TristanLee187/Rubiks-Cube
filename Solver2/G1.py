ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # U face
    [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # F face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # R face
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17],  # B face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17],  # L face
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # D face
    [i for i in range(18)]  # all allowed moves starting from no moves
]


def g1_all_good(cube):
    for i in cube.ops[:12]:
        if i == 0:
            return False
    return True


def g1_id_dfs(cube, depth, ans):
    def dfs(last):
        if len(ans) == depth:
            return g1_all_good(cube)
        else:
            for turn in ALLOWED_MOVES[last // 3]:
                cube.move(turn)
                ans.append(turn)
                found = dfs(turn)
                if found:
                    return True
                cube.undo(turn)
                ans.pop()

    attempt = dfs(-1)
    if attempt:
        return True
    ans.clear()
    g1_id_dfs(cube, depth + 1, ans)

G1_ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # U face
    [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # F face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # R face
    [0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17],  # B face
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
    def dfs(last, d, pans):
        if d == depth:
            return g1_all_good(cube)
        for turn in G1_ALLOWED_MOVES[last // 3]:
            cube.move(turn)
            found = dfs(turn, d+1, pans)
            if found:
                pans.append(turn)
                return True
            cube.undo(turn)

    sol = []
    attempt = dfs(-1, 0, sol)
    if attempt:
        ans += sol[::-1]
        return True
    g1_id_dfs(cube, depth + 1, ans)

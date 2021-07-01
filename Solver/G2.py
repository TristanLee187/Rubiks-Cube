G2_ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1],  # U face
    [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17],  # F face
    [3, 4, 5, 9, 10, 11, 12, 13, 14, 17],  # R face
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 17],  # B face
    [2, 3, 4, 5, 9, 10, 11, 17],  # L face
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # D face
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17]  # all allowed moves starting from no moves
]


def g2_all_good(cube):
    if sum(cube.ops[12:]):
        return False
    for i in [0, 2, 8, 10]:
        if cube.ps[i] not in [0, 2, 8, 10]:
            return False
    return True


def g2_id_dfs(cube, depth, ans):
    def dfs(last):
        if len(ans) == depth:
            return g2_all_good(cube)
        else:
            for turn in G2_ALLOWED_MOVES[last // 3]:
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
    g2_id_dfs(cube, depth + 1, ans)

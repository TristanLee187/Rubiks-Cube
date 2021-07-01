G4_ALLOWED_MOVES = [
    [5, 8, 11, 14, 17],  # U face
    [2, 8, 11, 14, 17],  # F face
    [5, 11, 14, 17],  # R face
    [5, 8, 14, 17],  # B face
    [2, 5, 11, 17],  # L face
    [5, 8, 11, 14],  # D face
    [2, 5, 8, 11, 14, 17]  # all allowed moves starting from no moves
]


def g4_all_good(cube):
    for i in range(20):
        if i != cube.ps[i]:
            return False
    return True


def g4_id_dfs(cube, depth, ans):
    def dfs(last):
        if len(ans) == depth:
            return g4_all_good(cube)
        else:
            for turn in G4_ALLOWED_MOVES[last // 3]:
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
    g4_id_dfs(cube, depth + 1, ans)

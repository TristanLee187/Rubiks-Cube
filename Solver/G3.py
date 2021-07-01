G3_ALLOWED_MOVES = [
    [5, 6, 7, 8, 11, 12, 13, 14, 17],  # U face
    [2, 6, 7, 8, 11, 12, 13, 14, 17],  # F face
    [5, 11, 12, 13, 14, 17],  # R face
    [5, 6, 7, 8, 12, 13, 14, 17],  # B face
    [2, 5, 11, 17],  # L face
    [5, 6, 7, 8, 11, 12, 13, 14],  # D face
    [2, 5, 6, 7, 8, 11, 12, 13, 14, 17]  # all allowed moves starting from no moves
]

C_OPPOSITES = [
    18, 17, 16, 19, 14, 13, 12, 15
]


def check_pieces(a, cube):
    for i in a:
        if cube.ps[i] not in a:
            return False
    return True


def c_check(a, cube):
    for i in a:
        s = cube.ps[i]
        if s not in a or s not in [i, C_OPPOSITES[i - 12]]:
            return False
    return True


def g3_all_good(cube):
    if not check_pieces([1, 3, 9, 11], cube):
        return False
    if not check_pieces([4, 5, 6, 7], cube):
        return False
    if not c_check([12, 13, 14, 15], cube):
        return False
    if not c_check([16, 17, 18, 19], cube):
        return False
    return True


def g3_id_dfs(cube, depth, ans):
    def dfs(last):
        if len(ans) == depth:
            return g3_all_good(cube)
        else:
            for turn in G3_ALLOWED_MOVES[last // 3]:
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
    g3_id_dfs(cube, depth + 1, ans)

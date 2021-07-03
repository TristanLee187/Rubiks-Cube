G3_ALLOWED_MOVES = [
    [5, 6, 7, 8, 11, 12, 13, 14, 17],  # U face
    [2, 6, 7, 8, 11, 12, 13, 14, 17],  # F face
    [2, 5, 11, 12, 13, 14, 17],  # R face
    [2, 6, 7, 8, 12, 13, 14, 17],  # B face
    [2, 5, 11, 17],  # L face
    [5, 6, 7, 8, 11, 12, 13, 14],  # D face
    [2, 5, 6, 7, 8, 11, 12, 13, 14, 17]  # all allowed moves starting from no moves
]

C_OPPOSITES = [
    14, 15, 12, 13, 18, 19, 16, 17
]


def check_pieces(a, cube):
    for i in a:
        if cube.ps[i] not in a:
            return False
    return True


def c_check(a, cube):
    e = 0
    for i in a:
        s = cube.ps[i]
        if s not in a or s not in [i, C_OPPOSITES[i - 12]]:
            return False
        if s == C_OPPOSITES[i - 12]:
            e += 1
    return e % 4 == 0


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
    def dfs(last, d, pans):
        if d == depth:
            return g3_all_good(cube)
        for turn in G3_ALLOWED_MOVES[last // 3]:
            cube.move(turn)
            found = dfs(turn, d + 1, pans)
            if found:
                pans.append(turn)
                return True
            cube.undo(turn)

    sol = []
    attempt = dfs(-1, 0, sol)
    if attempt:
        ans += sol[::-1]
        return True
    g3_id_dfs(cube, depth + 1, ans)

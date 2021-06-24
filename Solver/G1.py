# Good edges: can be solved without quarter turns of F or B (without F, F', B, or B')


t_checks = {1: 3, 3: 2, 5: 1, 7: 4}
b_checks = {1: 1, 3: 2, 5: 3, 7: 4}


def all_good(cube):
    # top face
    for i in range(1, 8, 2):
        s = cube.get_sticker(0, i)
        if s in [2, 4]:
            return False
        if s in [1, 3]:
            if cube.get_sticker(t_checks[i], 1) in [0, 5]:
                return False
    # bottom face
    for i in range(1, 8, 2):
        s = cube.get_sticker(5, i)
        if s in [2, 4]:
            return False
        if s in [1, 3]:
            if cube.get_sticker(b_checks[i], 5) in [0, 5]:
                return False
    # E slice
    if cube.front[3] in [2, 4] or (cube.front[3] in [1, 3] and cube.right[7] in [0, 5]):
        return False
    if cube.front[7] in [2, 4] or (cube.front[7] in [1, 3] and cube.left[3] in [0, 5]):
        return False
    if cube.back[3] in [2, 4] or (cube.back[3] in [1, 3] and cube.left[7] in [0, 5]):
        return False
    if cube.back[7] in [2, 4] or (cube.back[7] in [1, 3] and cube.right[3] in [0, 5]):
        return False
    return True


ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # U face
    [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # F face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # R face
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17],  # B face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17],  # L face
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # D face
    [i for i in range(18)]  # all allowed moves starting from no moves
]


def id_dfs(cube, depth, ans):
    def dfs(last):
        if len(ans) == depth:
            return all_good(cube)
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
    id_dfs(cube, depth + 1, ans)

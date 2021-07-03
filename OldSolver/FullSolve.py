# Checks for each stage
def g1_all_good(cube):
    for i in cube.ops[:12]:
        if i == 0:
            return False
    return True


def check_pieces(a, cube):
    for i in a:
        if cube.ps[i] not in a:
            return False
    return True


def g2_all_good(cube):
    if sum(cube.ops[12:]):
        return False
    if not check_pieces([0, 2, 8, 10], cube):
        return False
    return True


C_OPPOSITES = [
    14, 15, 12, 13, 18, 19, 16, 17
]


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


def g4_all_good(cube):
    for i in range(20):
        if i != cube.ps[i]:
            return False
    return True


CHECKS = [g1_all_good, g2_all_good, g3_all_good, g4_all_good]


# IDDFS
def id_dfs(cube, ans, check):
    def dfs(last, d, pans, depth):
        if d == depth:
            return CHECKS[check](cube)
        for turn in ALLOWED_MOVES[last // 3]:
            cube.move(turn)
            found = dfs(turn, d+1, pans, depth)
            if found:
                pans.append(turn)
                return True
            cube.undo(turn)

    i = 0
    while True:
        sol = []
        attempt = dfs(-1, 0, sol, i)
        if attempt:
            ans += sol[::-1]
            return True
        i += 1


# G1
ALLOWED_MOVES = [
    set(range(3, 18)),  # U face
    {0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17},  # F face
    {0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17},  # R face
    {0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17},  # B face
    {0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17},  # L face
    set(range(3, 15)),  # D face
    set(range(18))  # all allowed moves starting from no moves
]

REMOVE = [
    [0, 1, 15, 16],  # G2
    [3, 4, 9, 10],  # G3
    [6, 7, 12, 13],  # G4
    []
]


def scramble_num_to_str(scramble):
    ans = ''
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for num in scramble:
        add = moves[num // 3]
        add += ['', '\'', '2'][num % 3]
        ans += add + ' '
    return ans


def full_solve(cube):
    ans = []
    for i in range(4):
        sol = []
        id_dfs(cube, sol, i)
        ans += sol

        for move in ALLOWED_MOVES:
            for remove in REMOVE[i]:
                if remove in move:
                    move.remove(remove)

        print(scramble_num_to_str(sol))

    return ans

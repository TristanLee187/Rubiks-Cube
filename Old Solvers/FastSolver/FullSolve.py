from FastCube import FastCube
from collections import defaultdict

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
    [0, 1, 15, 16],  # remove these moves to get G1 moves
    [3, 4, 9, 10],  # G2
    [6, 7, 12, 13],  # G3
    []
]


def phase_solve(cube, goal, check):
    def clean_moves():
        for remove in REMOVE[check]:
            for i in range(7):
                if remove in ALLOWED_MOVES[i]:
                    ALLOWED_MOVES[i].remove(remove)

    cube.scramble = [-1]
    cube.phase_set(check)
    states = [cube]
    goal_state = goal.g_get(check)

    if states[0].g_get(check) == goal_state:
        clean_moves()
        return []

    while True:
        seen = set()
        new_states = []
        for cube_state in states:
            for move in ALLOWED_MOVES[cube_state.scramble[-1] // 3]:
                next_cube = cube_state.__copy__()
                next_cube.move(move)
                next_state = next_cube.g_get(check)
                if next_state == goal_state:
                    ans = next_cube.scramble[1:]
                    for turn in ans:
                        cube.move(turn)
                    clean_moves()
                    return ans
                if next_state not in seen:
                    seen.add(next_state)
                    new_states.append(next_cube)
        states = new_states.copy()


def sub_cond(c):
    collect = defaultdict(int)
    for move in c:
        turn = move % 3
        collect[move // 3] += (1 + (turn >> 1)) - 2 * (turn & 1)
    ans = []
    for move in collect:
        turns = collect[move] % 4
        if turns:
            turn = (turns >> 1) + (not (turns & 1))
            ans.append(3 * move + turn)
    return ans


def cond(s):
    axes = {0: 0, 15: 0, 3: 1, 9: 1, 6: 2, 12: 2}
    ans = [s[0]]
    p = 0
    for i in range(1, len(s)):
        move = s[i]
        axis = axes[move - move % 3]
        if not ans or axis != axes[ans[p] - ans[p] % 3]:
            ans.append(move)
            p = len(ans) - 1
        else:
            sub = sub_cond(ans[p:] + [move])
            ans[p:] = []
            ans += sub
            if not sub:
                p -= 1
    return ans


def full_solve(cube):
    g = FastCube()
    ans = []
    for i in range(4):
        ans += phase_solve(cube, g, i)
    return cond(ans)

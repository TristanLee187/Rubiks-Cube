G2_ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1],  # U face
    [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17],  # F face
    [3, 4, 5, 9, 10, 11, 12, 13, 14, 17],  # R face
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 17],  # B face
    [2, 3, 4, 5, 9, 10, 11, 17],  # L face
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # D face
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17]  # all allowed moves starting from no moves
]


def g2_state(cube):
    ans = 0
    i = 0
    while i < 12:
        ans |= (cube.ps[i] // 4 == 0) << i
        i += 1
    while i < 20:
        ans |= cube.ops[i] << (12 + 2 * (i - 12))
        i += 1
    return ans


def g2_solve(cube, goal):
    cube.scramble = [-1]
    states = [cube]
    goal_state = g2_state(goal)

    if states[0] == goal_state:
        return []

    seen = set()
    while True:
        new_states = []
        for cube_state in states:
            for move in G2_ALLOWED_MOVES[cube_state.scramble[-1] // 3]:
                next_cube = cube_state.__copy__()
                next_cube.move(move)
                next_state = g2_state(next_cube)
                if next_state == goal_state:
                    ans = next_cube.scramble[1:]
                    for turn in ans:
                        cube.move(turn)
                    return ans
                if next_state not in seen:
                    seen.add(next_state)
                    new_states.append(next_cube)
        states = new_states.copy()
        seen.clear()

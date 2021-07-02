G1_ALLOWED_MOVES = [
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # U face
    [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # F face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # R face
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17],  # B face
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17],  # L face
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # D face
    [i for i in range(18)]  # all allowed moves starting from no moves
]


def g1_state(cube):
    ans = 0
    for i in range(12):
        ans |= cube.ops[i] << i
    return ans


def g1_solve(cube, goal):
    cube.scramble = [-1]
    states = [cube]
    goal_state = g1_state(goal)

    if states[0] == goal_state:
        return []

    seen = set()
    while True:
        new_states = []
        for cube_state in states:
            for move in G1_ALLOWED_MOVES[cube_state.scramble[-1] // 3]:
                next_cube = cube_state.__copy__()
                next_cube.move(move)
                next_state = g1_state(next_cube)
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

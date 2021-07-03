G4_ALLOWED_MOVES = [
    [5, 8, 11, 14, 17],  # U face
    [2, 8, 11, 14, 17],  # F face
    [2, 5, 11, 14, 17],  # R face
    [2, 8, 14, 17],  # B face
    [2, 5, 11, 17],  # L face
    [5, 8, 11, 14],  # D face
    [2, 5, 8, 11, 14, 17]  # all allowed moves starting from no moves
]


def g4_state(cube):
    ans = 0
    for i in range(20):
        ans |= (cube.ps[i] == i) << i
    return ans


def g4_solve(cube, goal):
    cube.scramble = [-1]
    states = [cube]
    goal_state = g4_state(goal)

    if g4_state(states[0]) == goal_state:
        return []

    seen = set()
    while True:
        new_states = []
        for cube_state in states:
            for move in G4_ALLOWED_MOVES[cube_state.scramble[-1] // 3]:
                next_cube = cube_state.__copy__()
                next_cube.move(move)
                next_state = g4_state(next_cube)
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

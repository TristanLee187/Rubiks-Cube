# A single file containing the FactCube class and implementation of solving the cube via the 4 stages of
# Thistlethwaite's algorithm.
#
# At a high level, the algorithm works by progressing through 4 stages. The cube must meet certain requirements to reach
# each stage; once a stage is met, some moves are removed from the set of moves needed to solve the cube, such that the
# requirements of one stage carry over into the next.
#
# For example, the first stage consists of the set of any state of the cube (G0), and the set moves needed to reach the
# second stage (all 18 moves). For a cube to meet the requirements of the second stage, all the edges must be oriented
# such that they can be placed in their correct location in the correct orientation without quarter turns of the U and D
# face. Once this stage is reached, quarter turns of the U and D faces are removed from the set of allowed moves; now,
# when progressing to the third stage, all possible cube states will also meet the requirements of the second stage.
# Notice that any state in group i+1 is also in group i; i.e., the set of states in group i+1 is a subset of the states
# in group i. Progression is made in this manner until the fifth stage is reached; only one state meets the
# requirements for this stage: the solved state. See the corresponding files for details on each stage.
#
# We progress through the stages with iterative deepening depth first search (IDDFS). We start at depth 0. For any depth
# d, we generate all combinations of moves of length d given the allowed moves of the current stage. If one of these
# combinations moves the cube into the next stage, then we add it to the solution, and move on to the next stage,
# removing moves from teh set of allowed moves as appropriate.
# If none of the combinations work, then we increase the depth by 1 and generate all combinations of that length, check
# those, and so on. This incrementing of the depth ensures that the solution between stages is always the shortest
# possible length. The scramble field of each FastCube object keeps track of the moves applied to each instance.
# A note about generating combinations of moves: my implementation minds symmetry of turning faces along the same axis.
# For example, applying a U face turn (U, U', or U2) twice in a row can be captured by a single U face turn, so this
# should not be allowed. Also, applying a U move and then a D move has the same affect as applying the D move first then
# the U move, so only one of these should be allowed.
#
# At a lower level, I also use pruning to eliminate branches of this tree (which is very helpful considering branching
# factors of around 15). Though two different scrambles will very likely produce two different states, each stage
# considers only certain details about the current state to be important, based on its requirements. For example, the
# second stage only cares about the orientation of the edge pieces. Therefore, this stage will consider two states with
# the same orientation of edges at each location on the cube to be the same, even if the actual edge pieces at those
# locations are different, and regardless of any information about the corner pieces. This pruning reduces the maximum
# possible runtime from the order of trillions to just over one million (see https://www.jaapsch.net/puzzles/thistle.htm
# for these factors, as well as an overview of the algorithm from Thistlethwaite's papers). Programmatically, arrays of
# values can capture this information, but I use integers and bitwise operations to increase speed.


E_MOVES = [
            [0, 5, 1, 4], [4, 1, 5, 0], [0, 5, 1, 4],  # U moves
            [1, 9, 2, 10], [10, 2, 9, 1], [1, 9, 2, 10],  # F moves
            [5, 8, 6, 9], [9, 6, 8, 5], [5, 8, 6, 9],  # R moves
            [0, 11, 3, 8], [8, 3, 11, 0], [0, 11, 3, 8],  # B moves
            [4, 10, 7, 11], [11, 7, 10, 4], [4, 10, 7, 11],  # L moves
            [2, 6, 3, 7], [7, 3, 6, 2], [2, 6, 3, 7],  # D moves
        ]

C_MOVES = [
            [12, 13, 14, 15], [15, 14, 13, 12], [12, 13, 14, 15],  # U moves
            [15, 14, 18, 19], [19, 18, 14, 15], [15, 14, 18, 19],  # F moves
            [14, 13, 17, 18], [18, 17, 13, 14], [14, 13, 17, 18],  # R moves
            [13, 12, 16, 17], [17, 16, 12, 13], [13, 12, 16, 17],  # B moves
            [12, 15, 19, 16], [16, 19, 15, 12], [12, 15, 19, 16],  # L moves
            [19, 18, 17, 16], [16, 17, 18, 19], [19, 18, 17, 16]  # D moves
        ]

CO = [1, 2, 0, 2, 0, 1]


class FastCube:
    def __init__(self):
        self.ps = list(range(20))
        self.ops = 20 * [0]
        self.scramble = []

    def move(self, turn):
        if turn % 3 < 2:
            last = self.ps[E_MOVES[turn][3]]
            self.ps[E_MOVES[turn][3]], self.ps[E_MOVES[turn][2]], self.ps[E_MOVES[turn][1]] = \
                self.ps[E_MOVES[turn][2]], self.ps[E_MOVES[turn][1]], self.ps[E_MOVES[turn][0]]
            self.ps[E_MOVES[turn][0]] = last

            last = self.ops[E_MOVES[turn][3]]
            self.ops[E_MOVES[turn][3]], self.ops[E_MOVES[turn][2]], self.ops[E_MOVES[turn][1]] = \
                self.ops[E_MOVES[turn][2]], self.ops[E_MOVES[turn][1]], self.ops[E_MOVES[turn][0]]
            self.ops[E_MOVES[turn][0]] = last

            last = self.ps[C_MOVES[turn][3]]
            self.ps[C_MOVES[turn][3]], self.ps[C_MOVES[turn][2]], self.ps[C_MOVES[turn][1]] = \
                self.ps[C_MOVES[turn][2]], self.ps[C_MOVES[turn][1]], self.ps[C_MOVES[turn][0]]
            self.ps[C_MOVES[turn][0]] = last

            last = self.ops[C_MOVES[turn][3]]
            self.ops[C_MOVES[turn][3]], self.ops[C_MOVES[turn][2]], self.ops[C_MOVES[turn][1]] = \
                self.ops[C_MOVES[turn][2]], self.ops[C_MOVES[turn][1]], self.ops[C_MOVES[turn][0]]
            self.ops[C_MOVES[turn][0]] = last
        else:
            last3, last2 = self.ps[E_MOVES[turn][3]], self.ps[E_MOVES[turn][2]]
            self.ps[E_MOVES[turn][3]], self.ps[E_MOVES[turn][2]] = self.ps[E_MOVES[turn][1]], self.ps[
                E_MOVES[turn][0]]
            self.ps[E_MOVES[turn][0]], self.ps[E_MOVES[turn][1]] = last2, last3

            last3, last2 = self.ops[E_MOVES[turn][3]], self.ops[E_MOVES[turn][2]]
            self.ops[E_MOVES[turn][3]], self.ops[E_MOVES[turn][2]] = self.ops[E_MOVES[turn][1]], \
                                                                               self.ops[E_MOVES[turn][0]]
            self.ops[E_MOVES[turn][0]], self.ops[E_MOVES[turn][1]] = last2, last3

            last3, last2 = self.ps[C_MOVES[turn][3]], self.ps[C_MOVES[turn][2]]
            self.ps[C_MOVES[turn][3]], self.ps[C_MOVES[turn][2]] = self.ps[C_MOVES[turn][1]], self.ps[
                C_MOVES[turn][0]]
            self.ps[C_MOVES[turn][0]], self.ps[C_MOVES[turn][1]] = last2, last3

            last3, last2 = self.ops[C_MOVES[turn][3]], self.ops[C_MOVES[turn][2]]
            self.ops[C_MOVES[turn][3]], self.ops[C_MOVES[turn][2]] = self.ops[C_MOVES[turn][1]], \
                                                                               self.ops[C_MOVES[turn][0]]
            self.ops[C_MOVES[turn][0]], self.ops[C_MOVES[turn][1]] = last2, last3

        if turn // 3 in [0, 5] and turn % 3 < 2:
            for num in E_MOVES[turn]:
                self.ops[num] = 1 - self.ops[num]

        if turn % 3 < 2:
            for num in C_MOVES[turn]:
                self.ops[num] += self.ops[num] + CO[turn // 3]
                self.ops[num] %= 3

        self.scramble.append(turn)

    def undo(self, turn):
        self.move(3 * (turn // 3) + [1, 0, 2][turn % 3])

    def __str__(self):
        return ' '.join(map(str, self.ps)) + '\n' + ' '.join(map(str, self.ops))

    def __copy__(self):
        ans = FastCube()
        ans.ps = self.ps.copy()
        ans.ops = self.ops.copy()
        ans.scramble = self.scramble.copy()
        return ans


# G1 check
def g1_state(cube):
    ans = 0
    for i in range(12):
        ans |= cube.ops[i] << i
    return ans


# G2 check
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


# G3 check
C_OPPOSITES = [
    14, 15, 12, 13, 18, 19, 16, 17
]


def g3_state(cube):
    ans = 0
    i = 0
    e = 0
    while i < 12:
        ans |= (cube.ps[i] // 4) << (2 * i)
        i += 1
    while i < 20:
        ans |= (((cube.ps[i] // 4) & 1) | (2 * (cube.ps[i] in [i, C_OPPOSITES[i - 12]]))) << (2 * i)
        e += cube.ps[i] == C_OPPOSITES[i - 12]
        i += 1
    ans |= (e % 4) << (2 * i)
    return ans


# G4 check
def g4_state(cube):
    ans = 0
    for i in range(20):
        ans |= (cube.ps[i] == i) << i
    return ans


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


CHECKS = [g1_state, g2_state, g3_state, g4_state]


def scramble_num_to_str(scramble):
    ans = ''
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for num in scramble:
        add = moves[num // 3]
        add += ['', '\'', '2'][num % 3]
        ans += add + ' '
    return ans


def phase_solve(cube, goal, check):
    def clean_moves():
        for remove in REMOVE[check]:
            for i in range(7):
                if remove in ALLOWED_MOVES[i]:
                    ALLOWED_MOVES[i].remove(remove)

    cube.scramble = [-1]
    states = [cube]
    goal_state = CHECKS[check](goal)

    if CHECKS[check](states[0]) == goal_state:
        clean_moves()
        return []

    seen = set()
    while True:
        new_states = []
        for cube_state in states:
            for move in ALLOWED_MOVES[cube_state.scramble[-1] // 3]:
                next_cube = cube_state.__copy__()
                next_cube.move(move)
                next_state = CHECKS[check](next_cube)
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
        seen.clear()


def full_solve(cube):
    g = FastCube()
    ans = []
    for i in range(4):
        ans += phase_solve(cube, g, i)
    return ans

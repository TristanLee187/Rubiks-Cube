# Rubik's Cube class
# The cube is represented as an array of integers 0-19, each representing a corner or edge piece of the cube,
# and another array pf integers 0-2, the orientations of each of those pieces (0-1 for edges, 0-2 for corners).
# Moves performed on the cube are represented by integers 0-17. Let a be the set of these integers with
# a_i == 0 (modulo 3); a_i, a_i + 1, and a_i + 2 are the 90 degree clockwise turn, 90 degree counterclockwise turn, and
# 180 degree turn of each of the 6 faces.
# Each move affects 4 edge and 4 corner pieces, detailed in E_MOVES and C_MOVES; their positions and orientations
# change depending on the move.
# The following are the assignments of numbers to pieces, moves, and orientations.
#
# Numbers of the pieces:
#
#               12 0  13
#               4     5
#               15 1  14
#
#     12 4 15   15 1 14   14 5 13   13 0 12
#     11   10   10   9    9    8    8    11
#     16 7 19   19 2 18   18 6 17   17 3 16
#
#               19 2 18
#               7    6
#               16 3 17
#
#
# Edge orientation: a good edge can be solved without U or D moves; 0 if good, 1 if not
# Corner orientation: track left or right sticker; 0 if that sticker is facing along the x-axis, 1 for the z-axis,
#     and 2 for y-axis
#
#
# Numbers to moves:
#     0: U
#     3: F
#     6: R
#     9: B
#     12: L
#     15: D
# The scramble field is only used in solving the cube; it keeps track of the moves done on the cube in each
# of the Thistlethwaite algorithm's 4 stages.


from convert import *


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
    def __init__(self, layout=None):
        self.ps = list(range(20))
        self.ops = 20 * [0]
        self.scramble = []

        if layout:
            convert(layout, self)

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

            for num in C_MOVES[turn]:
                self.ops[num] += self.ops[num] + CO[turn // 3]
                self.ops[num] %= 3

            if turn // 3 in [0, 5]:
                for num in E_MOVES[turn]:
                    self.ops[num] = 1 - self.ops[num]
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

        self.scramble.append(turn)

    def __str__(self):
        return ' '.join(map(str, self.ps)) + '\n' + ' '.join(map(str, self.ops))

    def __copy__(self):
        ans = FastCube()
        ans.ps = self.ps.copy()
        ans.ops = self.ops.copy()
        ans.scramble = self.scramble.copy()
        return ans

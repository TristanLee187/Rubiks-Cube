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

class FastCube:
    def __init__(self):
        self.ps = list(range(20))
        self.ops = 12 * [1] + 8 * [0]
        self.e_moves = [
            [0, 1, 2, 3], [3, 2, 1, 0], [0, 1, 2, 3],  # U moves
            [2, 5, 10, 6], [6, 10, 5, 2], [2, 5, 10, 6],  # F moves
            [1, 4, 9, 5], [5, 9, 4, 1], [1, 4, 9, 5],  # R moves
            [0, 7, 8, 4], [4, 8, 7, 0], [0, 7, 8, 4],  # B moves
            [3, 6, 11, 7], [7, 11, 6, 3], [3, 6, 11, 7],  # L moves
            [10, 9, 8, 11], [11, 8, 9, 10], [10, 9, 8, 11],  # D moves
        ]
        self.c_moves = [
            [12, 13, 14, 15], [15, 14, 13, 12], [12, 13, 14, 15],  # U moves
            [15, 14, 18, 19], [19, 18, 14, 15], [15, 14, 18, 19],  # F moves
            [14, 13, 17, 18], [18, 17, 13, 14], [14, 13, 17, 18],  # R moves
            [13, 12, 16, 17], [17, 16, 12, 13], [13, 12, 16, 17],  # B moves
            [12, 15, 19, 16], [16, 19, 15, 12], [12, 15, 19, 16],  # L moves
            [19, 18, 17, 16], [16, 17, 18, 19], [19, 18, 17, 16]  # D moves
        ]
        self.co = [1, 2, 0, 2, 0, 1]

    def move(self, turn):
        if turn % 3 < 2:
            last = self.ps[self.e_moves[turn][3]]
            self.ps[self.e_moves[turn][3]], self.ps[self.e_moves[turn][2]], self.ps[self.e_moves[turn][1]] = \
                self.ps[self.e_moves[turn][2]], self.ps[self.e_moves[turn][1]], self.ps[self.e_moves[turn][0]]
            self.ps[self.e_moves[turn][0]] = last

            last = self.ops[self.e_moves[turn][3]]
            self.ops[self.e_moves[turn][3]], self.ops[self.e_moves[turn][2]], self.ops[self.e_moves[turn][1]] = \
                self.ops[self.e_moves[turn][2]], self.ops[self.e_moves[turn][1]], self.ops[self.e_moves[turn][0]]
            self.ops[self.e_moves[turn][0]] = last

            last = self.ps[self.c_moves[turn][3]]
            self.ps[self.c_moves[turn][3]], self.ps[self.c_moves[turn][2]], self.ps[self.c_moves[turn][1]] = \
                self.ps[self.c_moves[turn][2]], self.ps[self.c_moves[turn][1]], self.ps[self.c_moves[turn][0]]
            self.ps[self.c_moves[turn][0]] = last

            last = self.ops[self.c_moves[turn][3]]
            self.ops[self.c_moves[turn][3]], self.ops[self.c_moves[turn][2]], self.ops[self.c_moves[turn][1]] = \
                self.ops[self.c_moves[turn][2]], self.ops[self.c_moves[turn][1]], self.ops[self.c_moves[turn][0]]
            self.ops[self.c_moves[turn][0]] = last
        else:
            last3, last2 = self.ps[self.e_moves[turn][3]], self.ps[self.e_moves[turn][2]]
            self.ps[self.e_moves[turn][3]], self.ps[self.e_moves[turn][2]] = self.ps[self.e_moves[turn][1]], self.ps[
                self.e_moves[turn][0]]
            self.ps[self.e_moves[turn][0]], self.ps[self.e_moves[turn][1]] = last2, last3

            last3, last2 = self.ops[self.e_moves[turn][3]], self.ops[self.e_moves[turn][2]]
            self.ops[self.e_moves[turn][3]], self.ops[self.e_moves[turn][2]] = self.ops[self.e_moves[turn][1]], \
                                                                               self.ops[self.e_moves[turn][0]]
            self.ops[self.e_moves[turn][0]], self.ops[self.e_moves[turn][1]] = last2, last3

            last3, last2 = self.ps[self.c_moves[turn][3]], self.ps[self.c_moves[turn][2]]
            self.ps[self.c_moves[turn][3]], self.ps[self.c_moves[turn][2]] = self.ps[self.c_moves[turn][1]], self.ps[
                self.c_moves[turn][0]]
            self.ps[self.c_moves[turn][0]], self.ps[self.c_moves[turn][1]] = last2, last3

            last3, last2 = self.ops[self.c_moves[turn][3]], self.ops[self.c_moves[turn][2]]
            self.ops[self.c_moves[turn][3]], self.ops[self.c_moves[turn][2]] = self.ops[self.c_moves[turn][1]], \
                                                                               self.ops[self.c_moves[turn][0]]
            self.ops[self.c_moves[turn][0]], self.ops[self.c_moves[turn][1]] = last2, last3

        if turn // 3 in [0, 5] and turn % 3 < 2:
            for num in self.e_moves[turn]:
                self.ops[num] = 1 - self.ops[num]

        if turn % 3 < 2:
            for num in self.c_moves[turn]:
                self.ops[num] += self.ops[num] + self.co[turn // 3]
                self.ops[num] %= 3

    def undo(self, turn):
        self.move(3 * (turn // 3) + [1, 0, 2][turn % 3])

    def __str__(self):
        return ' '.join(map(str, self.ps)) + '\n' + ' '.join(map(str, self.ops))

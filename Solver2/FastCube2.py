class FastCube2:
    def __init__(self):
        self.ps = list(range(20))
        self.ops = 20 * [1]
        self.e_moves = [
            [0, 1, 2, 3], [3, 2, 1, 0], [0, 1, 2, 3],  # U moves
            [2, 5, 10, 6], [6, 10, 5, 2], [2, 5, 10, 6],  # F moves
            [1, 4, 9, 5], [5, 9, 4, 1], [1, 4, 9, 5],  # R moves
            [0, 7, 8, 4], [4, 8, 7, 0], [0, 7, 8, 4],  # B moves
            [3, 6, 11, 7], [7, 11, 6, 3], [3, 6, 11, 7],  # L moves
            [10, 9, 8, 11], [11, 8, 9, 10], [10, 9, 8, 11],  # D moves
        ]

    def move(self, turn):
        times = max(1, turn % 3)
        new = self.e_moves[turn].copy()
        for i in range(times):
            new.insert(0, new.pop())
        self.ops[self.e_moves[turn][0]], self.ops[self.e_moves[turn][1]], self.ops[self.e_moves[turn][2]], self.ops[
            self.e_moves[turn][3]] = self.ops[new[0]], self.ops[new[1]], self.ops[new[2]], self.ops[new[3]]

        self.ps[self.e_moves[turn][0]], self.ps[self.e_moves[turn][1]], self.ps[self.e_moves[turn][2]], self.ps[
            self.e_moves[turn][3]] = self.ps[new[0]], self.ps[new[1]], self.ps[new[2]], self.ps[new[3]]

        if turn // 3 in [0, 5] and turn % 3 < 2:
            for num in new:
                self.ops[num] = 1 - self.ops[num]

    def undo(self, turn):
        base = 3 * (turn // 3)
        add = [1, 0, 2][turn % 3]
        self.move(base + add)

    def __str__(self):
        return ' '.join(map(str, self.ps)) + '\n' + ' '.join(map(str, self.ops))

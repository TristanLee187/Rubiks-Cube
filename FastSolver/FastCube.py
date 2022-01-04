# Rubik's cube class similar to that found in Solver/, but each cube now stores its g1, g2, g3, and g4 states as fields,
# and moves affect these states directly. These objects have an array for representing piece locations, but not their
# orientations like the FastCubes of Solver/.

from convert import convert


class FastCube:
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

    G2_C_MOVES = [
        [12, 14, 16, 18], [18, 16, 14, 12], [12, 14, 16, 18],  # U moves
        [18, 16, 24, 26], [26, 24, 16, 18], [18, 16, 24, 26],  # F moves
        [16, 14, 22, 24], [24, 22, 14, 16], [16, 14, 22, 24],  # R moves
        [14, 12, 20, 22], [22, 20, 12, 14], [14, 12, 20, 22],  # B moves
        [12, 18, 26, 20], [20, 26, 18, 12], [12, 18, 26, 20],  # L moves
        [26, 24, 22, 20], [20, 22, 24, 26], [26, 24, 22, 20]  # D moves
    ]

    CO = [1, 2, 0, 2, 0, 1]

    C_OPPOSITES = [
        14, 15, 12, 13, 18, 19, 16, 17
    ]

    @staticmethod
    def rotate(a, b, c, offset):
        a[b[c][3]], a[b[c][2]], a[b[c][1]], a[b[c][0]] = \
            a[b[c][3 - offset]], a[b[c][2 - offset]], a[b[c][1 - offset]], a[b[c][0 - offset]]

    @staticmethod
    def g1_rotate(cube, turn, offset):
        a, b, c, d = FastCube.E_MOVES[turn]
        or_change = (turn // 3) in (0, 5) and offset & 1
        ba = (cube.g1 & (1 << a)) >> a ^ or_change
        bb = (cube.g1 & (1 << b)) >> b ^ or_change
        bc = (cube.g1 & (1 << c)) >> c ^ or_change
        bd = (cube.g1 & (1 << d)) >> d ^ or_change

        cube.g1 &= ((1 << 12) - 1) ^ ((1 << a) | (1 << b) | (1 << c) | (1 << d))

        cube.g1 |= (ba << (b if offset & 1 else c)) | (bb << (c if offset & 1 else d)) | \
                   (bc << (d if offset & 1 else a)) | (bd << (a if offset & 1 else b))

    @staticmethod
    def g2_rotate(cube, turn, offset):
        # edges
        a, b, c, d = FastCube.E_MOVES[turn]
        ba = (cube.g2 & (1 << a)) >> a
        bb = (cube.g2 & (1 << b)) >> b
        bc = (cube.g2 & (1 << c)) >> c
        bd = (cube.g2 & (1 << d)) >> d

        cube.g2 &= ((1 << 28) - 1) ^ ((1 << a) | (1 << b) | (1 << c) | (1 << d))

        cube.g2 |= (ba << (b if offset & 1 else c)) | (bb << (c if offset & 1 else d)) | \
                   (bc << (d if offset & 1 else a)) | (bd << (a if offset & 1 else b))

        # corners
        a, b, c, d = FastCube.G2_C_MOVES[turn]
        ba = (cube.g2 & (3 << a)) >> a
        bb = (cube.g2 & (3 << b)) >> b
        bc = (cube.g2 & (3 << c)) >> c
        bd = (cube.g2 & (3 << d)) >> d
        if offset & 1:
            ba = ((ba << 1) + FastCube.CO[turn // 3]) % 3
            bb = ((bb << 1) + FastCube.CO[turn // 3]) % 3
            bc = ((bc << 1) + FastCube.CO[turn // 3]) % 3
            bd = ((bd << 1) + FastCube.CO[turn // 3]) % 3

        cube.g2 &= ((1 << 28) - 1) ^ ((3 << a) | (3 << b) | (3 << c) | (3 << d))

        cube.g2 |= (ba << (b if offset & 1 else c)) | (bb << (c if offset & 1 else d)) | \
                   (bc << (d if offset & 1 else a)) | (bd << (a if offset & 1 else b))

    @staticmethod
    def g3_rotate(cube, turn, offset):
        # edges
        a, b, c, d = FastCube.E_MOVES[turn]
        a <<= 1
        b <<= 1
        c <<= 1
        d <<= 1
        ba = (cube.g3 & (3 << a)) >> a
        bb = (cube.g3 & (3 << b)) >> b
        bc = (cube.g3 & (3 << c)) >> c
        bd = (cube.g3 & (3 << d)) >> d

        cube.g3 &= ((1 << 42) - 1) ^ ((3 << a) | (3 << b) | (3 << c) | (3 << d))

        cube.g3 |= (ba << (b if offset & 1 else c)) | (bb << (c if offset & 1 else d)) | \
                   (bc << (d if offset & 1 else a)) | (bd << (a if offset & 1 else b))

        # corners
        a, b, c, d = FastCube.C_MOVES[turn]
        d_a = (cube.ps[a] in [a, FastCube.C_OPPOSITES[a - 12]]) << 1
        d_b = (cube.ps[b] in [b, FastCube.C_OPPOSITES[b - 12]]) << 1
        d_c = (cube.ps[c] in [c, FastCube.C_OPPOSITES[c - 12]]) << 1
        d_d = (cube.ps[d] in [d, FastCube.C_OPPOSITES[d - 12]]) << 1

        ba = ((cube.ps[a] >> 2) & 1) | d_a
        bb = ((cube.ps[b] >> 2) & 1) | d_b
        bc = ((cube.ps[c] >> 2) & 1) | d_c
        bd = ((cube.ps[d] >> 2) & 1) | d_d

        cube.g3 &= ((1 << 42) - 1) ^ ((3 << 40) | (3 << (a << 1)) | (3 << (b << 1)) | (3 << (c << 1)) | (3 << (d << 1)))

        cube.g3 |= (ba << (a << 1)) | (bb << (b << 1)) | \
                   (bc << (c << 1)) | (bd << (d << 1))

        e = 0
        for num in range(12, 20):
            e += cube.ps[num] == FastCube.C_OPPOSITES[num - 12]

        cube.g3 |= (e % 4) << 40

    @staticmethod
    def g4_rotate(cube, turn, offset):
        ans = 0
        for i in range(20):
            ans |= (cube.ps[i] == i) << i
        cube.g4 = ans

    @staticmethod
    def g3_state(cube):
        ans = 0
        i = 0
        e = 0
        while i < 12:
            ans |= (cube.ps[i] // 4) << (2 * i)
            i += 1
        while i < 20:
            ans |= (((cube.ps[i] // 4) & 1) | (2 * (cube.ps[i]
                                                    in [i, FastCube.C_OPPOSITES[i - 12]]))) << (2 * i)
            e += cube.ps[i] == FastCube.C_OPPOSITES[i - 12]
            i += 1
        ans |= (e % 4) << (2 * i)
        return ans

    @staticmethod
    def g4_state(cube):
        ans = 0
        for i in range(20):
            ans |= (cube.ps[i] == i) << i
        return ans

    @staticmethod
    def ps_rotate(cube, turn, offset):
        FastCube.rotate(cube.ps, FastCube.E_MOVES, turn, offset)
        FastCube.rotate(cube.ps, FastCube.C_MOVES, turn, offset)

    FUNCS = [
        [g1_rotate.__get__(object), g2_rotate.__get__(object)],
        [g2_rotate.__get__(object)],
        [g3_rotate.__get__(object)],
        [g4_rotate.__get__(object)]
    ]

    def __init__(self, layout=None):
        self.g1 = 0
        self.g2 = 15
        self.g3 = 734433793280
        self.g4 = 1048575
        self.ps = list(range(20))
        self.scramble = []
        self.phase = 0
        if layout:
            convert(layout, self)

    def move(self, turn):
        offset = ((turn % 3) >> 1) + 1
        FastCube.ps_rotate(self, turn, offset)
        for f in self.FUNCS[self.phase]:
            f(self, turn, offset)
        self.scramble.append(turn)

    def phase_set(self, phase):
        self.phase = phase
        if phase == 0:
            self.g3 = 0
            self.g4 = 0
        elif phase == 1:
            self.g1 = 0
        elif phase == 2:
            self.g2 = 0
            self.g3 = FastCube.g3_state(self)
        else:
            self.g3 = 0
            self.g4 = FastCube.g4_state(self)

    def g_get(self, phase):
        return [self.g1, self.g2, self.g3, self.g4][phase]

    def __copy__(self):
        ans = FastCube()
        ans.g1 = self.g1
        ans.g2 = self.g2
        ans.g3 = self.g3
        ans.g4 = self.g4
        ans.ps = self.ps.copy()
        ans.scramble = self.scramble.copy()
        ans.phase = self.phase
        return ans

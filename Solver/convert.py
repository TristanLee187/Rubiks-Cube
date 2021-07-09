# file for converting a string representing a cube from the Logic package to a FastCube object


PIECE_LAYOUT = [12, 0, 13, 4, -1, 5, 15, 1, 14, 12, 4, 15, 15, 1, 14, 14, 5, 13, 13, 0, 12, 11, -1, 10, 10, -1, 9, 9,
                -1, 8, 8, -1, 11, 16, 7, 19, 19, 2, 18, 18, 6, 17, 17, 3, 16, 19, 2, 18, 7, -1, 6, 16, 3, 17]

PIECES_NUMS_TO_COLORS = [('B', 'W'), ('G', 'W'), ('G', 'Y'), ('B', 'Y'), ('O', 'W'), ('R', 'W'), ('R', 'Y'), ('O', 'Y'),
                         ('B', 'R'), ('G', 'R'), ('G', 'O'), ('B', 'O'), ('B', 'O', 'W'), ('B', 'R', 'W'),
                         ('G', 'R', 'W'), ('G', 'O', 'W'), ('B', 'O', 'Y'), ('B', 'R', 'Y'), ('G', 'R', 'Y'),
                         ('G', 'O', 'Y')]

PIECES_COLORS_TO_NUMS = {('B', 'W'): 0, ('G', 'W'): 1, ('G', 'Y'): 2, ('B', 'Y'): 3, ('O', 'W'): 4, ('R', 'W'): 5,
                         ('R', 'Y'): 6, ('O', 'Y'): 7, ('B', 'R'): 8, ('G', 'R'): 9, ('G', 'O'): 10, ('B', 'O'): 11,
                         ('B', 'O', 'W'): 12, ('B', 'R', 'W'): 13, ('G', 'R', 'W'): 14, ('G', 'O', 'W'): 15,
                         ('B', 'O', 'Y'): 16, ('B', 'R', 'Y'): 17, ('G', 'R', 'Y'): 18, ('G', 'O', 'Y'): 19}


FACES = [
    list(range(9)),
    [12, 13, 14, 24, 25, 26, 36, 37, 38],
    [15, 16, 17, 27, 28, 29, 39, 40, 41],
    [18, 19, 20, 30, 31, 32, 42, 43, 44],
    [9, 10, 11, 21, 22, 23, 33, 34, 35],
    list(range(45, 54))
]


def def_piece(piece):
    ans = [-1, -1]
    ans[0] = PIECES_COLORS_TO_NUMS[tuple(sorted([i[0] for i in piece]))]
    stickers = {}
    n = len(piece)
    for i in range(6):
        for j in range(n):
            if piece[j][1] in FACES[i]:
                stickers[i] = piece[j][0]
    if n == 2:  # edge
        if 1 in stickers or 3 in stickers:
            look = 1 if 1 in stickers else 3
            if stickers[look] in 'RO':
                ans[1] = 1
            elif stickers[look] in 'WY' and ('G' in stickers.values() or 'B' in stickers.values()):
                ans[1] = 1
            else:
                ans[1] = 0
        else:
            look = 2 if 2 in stickers else 4
            if stickers[look] in 'GB':
                ans[1] = 1
            elif stickers[look] in 'WY' and ('R' in stickers.values() or 'O' in stickers.values()):
                ans[1] = 1
            else:
                ans[1] = 0
    else:
        check = 'R' if 'R' in stickers.values() else 'O'
        axis = [i for i in stickers if stickers[i] == check][0]
        if axis in [2, 4]:
            ans[1] = 0
        elif axis in [0, 5]:
            ans[1] = 2
        else:
            ans[1] = 1
    return ans


def convert(layout, cube):
    stickers = layout.split()
    z = list(zip(PIECE_LAYOUT, stickers))
    pieces = [[] for _ in range(20)]
    for i in range(54):
        entry = z[i]
        if entry[0] != -1:
            pieces[entry[0]] += [(entry[1], i)]
    for i in range(20):
        ans = def_piece(pieces[i])
        cube.ps[i] = ans[0]
        cube.ops[i] = ans[1]

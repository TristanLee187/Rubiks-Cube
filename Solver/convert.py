# file for converting a string representing a cube from the Logic package to a FastCube object


PIECE_LAYOUT = [12, 0, 13, 4, -1, 5, 15, 1, 14, 12, 4, 15, 15, 1, 14, 14, 5, 13, 13, 0, 12, 11, -1, 10, 10, -1, 9, 9,
                -1, 8, 8, -1, 11, 16, 7, 19, 19, 2, 18, 18, 6, 17, 17, 3, 16, 19, 2, 18, 7, -1, 6, 16, 3, 17]

FACES = [
    list(range(9)),
    [12, 13, 14, 24, 25, 26, 36, 37, 38],
    [15, 16, 17, 27, 28, 29, 39, 40, 41],
    [18, 19, 20, 30, 31, 32, 42, 43, 44],
    [9, 10, 11, 21, 22, 23, 33, 34, 35],
    list(range(45, 54))
]


def def_piece(piece, colors_to_nums, top_color, left_color, front_color, right_color, back_color, bottom_color):
    ans = [-1, -1]
    ans[0] = colors_to_nums[tuple(sorted([i[0] for i in piece]))]
    stickers = {}
    n = len(piece)
    for i in range(6):
        for j in range(n):
            if piece[j][1] in FACES[i]:
                stickers[i] = piece[j][0]
    if n == 2:  # edge
        if 1 in stickers or 3 in stickers:
            look = 1 if 1 in stickers else 3
            if stickers[look] in [right_color, left_color]:
                ans[1] = 1
            elif stickers[look] in [top_color, bottom_color] and \
                    (front_color in stickers.values() or back_color in stickers.values()):
                ans[1] = 1
            else:
                ans[1] = 0
        else:
            look = 2 if 2 in stickers else 4
            if stickers[look] in [front_color, back_color]:
                ans[1] = 1
            elif stickers[look] in [top_color, bottom_color] and \
                    (right_color in stickers.values() or left_color in stickers.values()):
                ans[1] = 1
            else:
                ans[1] = 0
    else:
        check = right_color if right_color in stickers.values() else left_color
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
    top_color = stickers[4]
    left_color = stickers[22]
    front_color = stickers[25]
    right_color = stickers[28]
    back_color = stickers[31]
    bottom_color = stickers[49]
    pieces_colors_to_nums = {(back_color, top_color): 0, (front_color, top_color): 1, (front_color, bottom_color): 2,
                             (back_color, bottom_color): 3, (left_color, top_color): 4, (right_color, top_color): 5,
                             (right_color, bottom_color): 6, (left_color, bottom_color): 7,
                             (back_color, right_color): 8, (front_color, right_color): 9, (front_color, left_color): 10,
                             (back_color, left_color): 11, (back_color, left_color, top_color): 12,
                             (back_color, right_color, top_color): 13, (front_color, right_color, top_color): 14,
                             (front_color, left_color, top_color): 15, (back_color, left_color, bottom_color): 16,
                             (back_color, right_color, bottom_color): 17, (front_color, right_color, bottom_color): 18,
                             (front_color, left_color, bottom_color): 19}
    pieces_colors_to_nums = {tuple(sorted([i[0] for i in piece])):pieces_colors_to_nums[piece] for piece in
                             pieces_colors_to_nums}
    z = list(zip(PIECE_LAYOUT, stickers))
    pieces = [[] for _ in range(20)]
    for i in range(54):
        entry = z[i]
        if entry[0] != -1:
            pieces[entry[0]] += [(entry[1], i)]
    for i in range(20):
        ans = def_piece(pieces[i], pieces_colors_to_nums, top_color, left_color, front_color, right_color, back_color,
                        bottom_color)
        cube.ps[i] = ans[0]
        cube.ops[i] = ans[1]

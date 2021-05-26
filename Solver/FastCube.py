import time


def rotate_ba(clock, ba):
    if clock:
        ans = ba[6:] + ba[:6]
    else:
        ans = ba[2:] + ba[:2]
    return ans


class FastCube:
    def __init__(self):
        self.front = 8 * [1]
        self.back = 8 * [3]
        self.top = 8 * [0]
        self.bottom = 8 * [5]
        self.right = 8 * [2]
        self.left = 8 * [4]
        self.colors = {0: 'W', 1: 'G', 2: 'R', 3: 'B', 4: 'O', 5: 'Y'}

    def __str__(self):
        arr = [3 * [' '] for i in range(3)]
        ans = 11 * ['']

        def face2str(barr, face, colors):
            indices = [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]]
            for i in range(8):
                sticker = barr[i]
                c = colors[sticker]
                x, y = indices[i]
                face[x][y] = c + ' '
            face[1][1] = '  '

        faces = [self.top, self.left, self.front, self.right, self.back, self.bottom]
        for i in range(6):
            face2str(faces[i], arr, self.colors)
            for row in range(3):
                add = ''.join(arr[row])
                if i == 0:
                    ans[row] += 9 * ' ' + add
                elif i == 5:
                    ans[8 + row] += 9 * ' ' + add
                else:
                    ans[4 + row] += add + '   '

        return '\n'.join(ans)

    def R(self, clock):
        self.right = rotate_ba(clock, self.right)
        back_row = self.back[6:] + self.back[:1]
        faces = [self.top, self.bottom]
        if not clock:
            faces[0], faces[1] = faces[1], faces[0]
        self.back[0], self.back[6:] = faces[0][4], faces[0][2:4]
        faces[0][2:5] = self.front[2:5]
        self.front[2:5] = faces[1][2:5]
        faces[1][2:5] = back_row

    def L(self, clock):
        self.left = rotate_ba(clock, self.left)
        back_row = self.back.copy()
        faces = [self.bottom, self.top]
        if not clock:
            faces[0], faces[1] = faces[1], faces[0]
        self.back[2:4], self.back[4] = faces[0][6:], faces[0][0]
        faces[0][0], faces[0][6:] = self.front[0], self.front[6:]
        self.front[0], self.front[6:] = faces[1][0], faces[1][6:]
        faces[1][0], faces[1][6:] = back_row[4], back_row[2:4]

    def U(self, clock):
        self.top = rotate_ba(clock, self.top)
        front_row = self.front[:3]
        faces = [self.front, self.right, self.back, self.left]
        if not clock:
            faces[1], faces[3] = faces[3], faces[1]
        for i in range(3):
            faces[i][:3] = faces[i + 1][:3]
        faces[3][:3] = front_row

    def D(self, clock):
        self.bottom = rotate_ba(clock, self.bottom)
        front_row = self.front[4:7]
        faces = [self.front, self.left, self.back, self.right]
        if not clock:
            faces[1], faces[3] = faces[3], faces[1]
        for i in range(3):
            faces[i][4:7] = faces[i + 1][4:7]
        faces[3][4:7] = front_row

    def F(self, clock):
        self.front = rotate_ba(clock, self.front)
        top_row = self.top.copy()
        if clock:
            self.top[4:7] = self.left[2:5]
            self.left[2:5] = self.bottom[:3]
            self.bottom[:2] = self.right[6:]
            self.bottom[2] = self.right[0]
            self.right[6:] = top_row[4:6]
            self.right[0] = top_row[6]
        else:
            self.top[4:6] = self.right[6:]
            self.top[6] = self.right[0]
            self.right[6:] = self.bottom[:2]
            self.right[0] = self.bottom[2]
            self.bottom[:3] = self.left[2:5]
            self.left[2:5] = top_row[4:7]

    def B(self, clock):
        self.back = rotate_ba(clock, self.back)
        top_row = self.top.copy()
        if clock:
            self.top[:3] = self.right[2:5]
            self.right[2:5] = self.bottom[4:7]
            self.bottom[4:6] = self.left[6:]
            self.bottom[6] = self.left[0]
            self.left[6:] = top_row[:2]
            self.left[0] = top_row[2]
        else:
            self.top[:2] = self.left[6:]
            self.top[2] = self.left[0]
            self.left[0] = self.bottom[6]
            self.left[6:] = self.bottom[4:6]
            self.bottom[4:7] = self.right[2:5]
            self.right[2:5] = top_row[:3]


def rta():
    t0 = time.time()
    c = FastCube()
    i = 0
    while i < 10 ** 6:
        c.R(False)
        c.F(True)
        c.R(True)
        c.F(False)
        i += 1
    t1 = time.time()
    print(c)
    print("Time:", t1 - t0)


def test_moves():
    c = FastCube()
    s = ['R','U','F','L','D','B','B\'', 'D\'', 'L\'', 'F\'', 'U\'', 'R\'']
    for move in s:
        eval('c.{}({})'.format(move[0], len(move) == 1))
    print(c)


# rta()
test_moves()

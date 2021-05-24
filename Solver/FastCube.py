from bitarray import *
import time


def rotate_ba(clock, ba):
    if clock:
        ba = ba[18:] + ba[:18]
    else:
        ba = ba[6:] + ba[:6]


class FastCube:
    def __init__(self):
        self.front = bitarray(8 * '001')
        self.back = bitarray(8 * '011')
        self.top = bitarray(8 * '000')
        self.bottom = bitarray(8 * '101')
        self.right = bitarray(8 * '010')
        self.left = bitarray(8 * '100')
        self.colors = {'W': '000', 'G': '001', 'R': '010', 'B': '011', 'O': '100', 'Y': '101'}

    def __str__(self):
        arr = [3 * [' '] for i in range(3)]
        ans = ''

        def face2str(barr, face, colors):
            indices = [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]]
            for i in range(0, 24, 3):
                sticker = barr[i:i + 3].to01()
                c = ''
                for color in colors:
                    if colors[color] == sticker:
                        c = color
                        break
                x, y = indices[i // 3]
                face[x][y] = c

        faces = [self.front, self.top, self.right, self.back, self.bottom, self.left]
        ids = ['Front', 'Top', 'Right', 'Back', 'Bottom', 'Left']
        for i in range(6):
            face2str(faces[i], arr, self.colors)
            ans += ids[i] + '\n'
            for row in arr:
                ans += ''.join(row) + '\n'

        return ans

    def R(self, clock):
        rotate_ba(clock, self.right)
        back_row = self.back[18:]+self.back[:3]
        if clock:
            self.back[:3] = self.top[12:15]
            self.back[18:24] = self.top[6:12]
            self.top[6:15] = self.front[6:15]
            self.front[6:15] = self.bottom[6:15]
            self.bottom[6:15] = back_row
        else:
            self.back[:3] = self.bottom[12:15]
            self.back[18:24] = self.bottom[6:12]
            self.bottom[6:15] = self.front[6:15]
            self.front[6:15] = self.top[6:15]
            self.top[6:15] = back_row

    def L(self, clock):
        rotate_ba(clock, self.left)
        back_row = self.back[6:15]

    def U(self, clock):
        rotate_ba(clock, self.top)
        front_row = self.front[:9]
        if clock:
            self.front[:9] = self.right[:9]
            self.right[:9] = self.back[:9]
            self.back[:9] = self.left[:9]
            self.left[:9] = front_row
        else:
            self.front[:9] = self.left[:9]
            self.left[:9] = self.back[:9]
            self.back[:9] = self.right[:9]
            self.right[:9] = front_row


def rta():
    t0 = time.time()
    c = FastCube()
    i = 0
    while i < 10 ** 6:
        c.R(True)
        i += 1
    t1 = time.time()
    print(c)
    print("Time:", t1 - t0)


rta()

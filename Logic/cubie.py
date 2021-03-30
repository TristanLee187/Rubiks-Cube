# class of cubie objects, each representing a single piece of the cube.

class cubie:
    # treat each cubie as a small cube with 6 faces; faces of the cubie that one wouldn't normally see
    # are given the color Black or 'BL'. The other colors are:
    # 'W': White
    # 'Y': Yellow
    # 'R': Red
    # 'O': Orange
    # 'B': Blue
    # 'G': Green

    def __init__(self, colors):
        self.right = colors[0]
        self.left = colors[1]
        self.top = colors[2]
        self.bottom = colors[3]
        self.front = colors[4]
        self.back = colors[5]

    # general rotate method, which calls on axis specific methods and passing along a boolean "clock";
    # this represents a clockwise turn if True and counterclockwise if False
    def rotate(self, axis, clock):
        if axis == 'x':
            self.rotate_x(clock)
        elif axis == 'y':
            self.rotate_y(clock)
        else:
            self.rotate_z(clock)

    def rotate_x(self, clock):
        if clock:
            self.top, self.front, self.bottom, self.back = self.front, self.bottom, self.back, self.top
        else:
            self.top, self.front, self.bottom, self.back = self.back, self.top, self.front, self.bottom

    def rotate_y(self, clock):
        if clock:
            self.right, self.front, self.left, self.back = self.back, self.right, self.front, self.left
        else:
            self.right, self.front, self.left, self.back = self.front, self.left, self.back, self.right

    def rotate_z(self, clock):
        if clock:
            self.top, self.right, self.bottom, self.left = self.left, self.top, self.right, self.bottom
        else:
            self.top, self.right, self.bottom, self.left = self.right, self.bottom, self.left, self.top

    def __str__(self):
        ans = ''
        ans += 'right: ' + self.right + '\n'
        ans += 'left: ' + self.left + '\n'
        ans += 'top: ' + self.top + '\n'
        ans += 'bottom: ' + self.bottom + '\n'
        ans += 'front: ' + self.front + '\n'
        ans += 'back: ' + self.back + '\n'
        return ans

# testing
# c=cubie(['BL','BL','W','BL','BL','BL'])
# c.rotate('z',True)
# c.rotate('y',True)
# l=[c]
# print(c)

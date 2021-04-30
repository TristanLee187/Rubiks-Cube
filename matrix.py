from math import sin, cos


# multiply m1 by m2, modifying m2 to be the product
# m1 * m2 -> m2
def matrix_mult(m1, m2):
    point = 0
    for row in m2:
        # get a copy of the next point
        tmp = row[:]

        for r in range(4):
            m2[point][r] = (m1[0][r] * tmp[0] +
                            m1[1][r] * tmp[1] +
                            m1[2][r] * tmp[2] +
                            m1[3][r] * tmp[3])
        point += 1


def rotation_matrix(theta, u):
    ans = [[cos(theta) + u[0] ** 2 * (1 - cos(theta)),
            u[0] * u[1] * (1 - cos(theta)) - u[2] * sin(theta),
            u[0] * u[2] * (1 - cos(theta)) + u[1] * sin(theta)],
           [u[0] * u[1] * (1 - cos(theta)) + u[2] * sin(theta),
            cos(theta) + u[1] ** 2 * (1 - cos(theta)),
            u[1] * u[2] * (1 - cos(theta)) - u[0] * sin(theta)],
           [u[0] * u[2] * (1 - cos(theta)) - u[1] * sin(theta),
            u[1] * u[2] * (1 - cos(theta)) + u[0] * sin(theta),
            cos(theta) + u[2] ** 2 * (1 - cos(theta))]]
    for i in range(3):
        ans[i].append(0)
    ans.append([0, 0, 0, 0])
    return ans

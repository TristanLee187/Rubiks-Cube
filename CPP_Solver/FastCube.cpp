#include <vector>
#include <iostream>
using namespace std;

short E_MOVES[18][4] = {
    {0, 5, 1, 4}, {4, 1, 5, 0}, {0, 5, 1, 4}, {1, 9, 2, 10}, {10, 2, 9, 1}, {1, 9, 2, 10}, {5, 8, 6, 9}, {9, 6, 8, 5}, {5, 8, 6, 9}, {0, 11, 3, 8}, {8, 3, 11, 0}, {0, 11, 3, 8}, {4, 10, 7, 11}, {11, 7, 10, 4}, {4, 10, 7, 11}, {2, 6, 3, 7}, {7, 3, 6, 2}, {2, 6, 3, 7}};

short C_MOVES[18][4] = {
    {12, 13, 14, 15}, {15, 14, 13, 12}, {12, 13, 14, 15}, {15, 14, 18, 19}, {19, 18, 14, 15}, {15, 14, 18, 19}, {14, 13, 17, 18}, {18, 17, 13, 14}, {14, 13, 17, 18}, {13, 12, 16, 17}, {17, 16, 12, 13}, {13, 12, 16, 17}, {12, 15, 19, 16}, {16, 19, 15, 12}, {12, 15, 19, 16}, {19, 18, 17, 16}, {16, 17, 18, 19}, {19, 18, 17, 16}};

short CO[] = {1, 2, 0, 2, 0, 1};

void rotate(vector<short> &a, short b[][4], int c, int offset)
{
    int n = a.size();
    short w = a[b[c][(offset == 2) * 2 + (offset == 1) * 3]];
    short x = a[b[c][(offset == 2) * 3]];
    short y = a[b[c][2 - offset]];
    short z = a[b[c][3 - offset]];
    a[b[c][0]] = w;
    a[b[c][1]] = x;
    a[b[c][2]] = y;
    a[b[c][3]] = z;
}

struct FastCube
{
    vector<short> ps;
    vector<short> ops;
    vector<short> scramble;

    FastCube()
    {
        for (short i = 0; i < 20; i++)
        {
            ps.push_back(i);
            ops.push_back(0);
        }
    }

    void move(short turn)
    {
        short offset = ((turn % 3) >> 1) + 1;
        rotate(ps, E_MOVES, turn, offset);
        rotate(ops, E_MOVES, turn, offset);
        rotate(ps, C_MOVES, turn, offset);
        rotate(ops, C_MOVES, turn, offset);
        if (offset == 1)
        {
            for (short num : C_MOVES[turn])
            {
                ops[num] += ops[num] + CO[turn / 3];
                ops[num] %= 3;
            }
            if (turn / 3 == 0 || turn / 3 == 5)
            {
                for (short num : E_MOVES[turn])
                    ops[num] ^= 1;
            }
        }
        scramble.push_back(turn);
    }
    string toString()
    {
        string strps;
        for (int i = 0; i < 20; i++)
            strps += to_string(ps[i]) + " ";

        string strops;
        for (int i = 0; i < 20; i++)
            strops += to_string(ops[i]) + " ";

        strps += "\n";
        strops += "\n";
        return strps + strops;
    }
};

int main()
{
    FastCube cube;
    FastCube cube2 = cube;
    cube.move(0);
    cout << cube.toString();
    cout << cube2.toString();
    return 0;
}
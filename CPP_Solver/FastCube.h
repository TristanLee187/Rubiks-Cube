/*
 * C++ implementation of the FastCube struct
 */

#include <vector>
#include <string>
using namespace std;

int E_MOVES[18][4] = {
    {0, 5, 1, 4}, {4, 1, 5, 0}, {0, 5, 1, 4}, {1, 9, 2, 10}, {10, 2, 9, 1}, {1, 9, 2, 10}, {5, 8, 6, 9}, {9, 6, 8, 5}, {5, 8, 6, 9}, {0, 11, 3, 8}, {8, 3, 11, 0}, {0, 11, 3, 8}, {4, 10, 7, 11}, {11, 7, 10, 4}, {4, 10, 7, 11}, {2, 6, 3, 7}, {7, 3, 6, 2}, {2, 6, 3, 7}};

int C_MOVES[18][4] = {
    {12, 13, 14, 15}, {15, 14, 13, 12}, {12, 13, 14, 15}, {15, 14, 18, 19}, {19, 18, 14, 15}, {15, 14, 18, 19}, {14, 13, 17, 18}, {18, 17, 13, 14}, {14, 13, 17, 18}, {13, 12, 16, 17}, {17, 16, 12, 13}, {13, 12, 16, 17}, {12, 15, 19, 16}, {16, 19, 15, 12}, {12, 15, 19, 16}, {19, 18, 17, 16}, {16, 17, 18, 19}, {19, 18, 17, 16}};

int CO[] = {1, 2, 0, 2, 0, 1};

void rotate(vector<int> &a, int b[][4], int c, int offset)
{
    int w = a[b[c][(offset==2) ? 2:3]];
    int x = a[b[c][(offset==2) ? 3:0]];
    int y = a[b[c][2 - offset]];
    int z = a[b[c][3 - offset]];
    a[b[c][0]] = w;
    a[b[c][1]] = x;
    a[b[c][2]] = y;
    a[b[c][3]] = z;
}

vector<string> split(string s)
{
    vector<string> ans;
    string word = "";
    for (int i = 0; i < s.size(); i++)
    {
        string c = s.substr(i, 1);
        if (c == " ")
        {
            ans.push_back(word);
            word = "";
        }
        else
        {
            word += c;
        }
    }
    if (word != " ")
        ans.push_back(word);
    return ans;
}

struct FastCube
{
    vector<int> ps;
    vector<int> ops;
    vector<int> scramble;

    FastCube()
    {
        for (int i = 0; i < 20; i++)
        {
            ps.push_back(i);
            ops.push_back(0);
        }
    }

    FastCube(string layout)
    {
        vector<string> layout_vector = split(layout);
        for (int i = 0; i < 20; i++)
        {
            ps.push_back(stoi(layout_vector[i]));
            ops.push_back(stoi(layout_vector[20 + i]));
        }
    }

    void move(int turn)
    {
        int offset = ((turn % 3) >> 1) + 1;
        rotate(ps, E_MOVES, turn, offset);
        rotate(ops, E_MOVES, turn, offset);
        rotate(ps, C_MOVES, turn, offset);
        rotate(ops, C_MOVES, turn, offset);
        if (offset == 1)
        {
            for (int num : C_MOVES[turn])
            {
                ops[num] += ops[num] + CO[turn / 3];
                ops[num] %= 3;
            }
            if (turn / 3 == 0 || turn / 3 == 5)
            {
                for (int num : E_MOVES[turn])
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

#include "FastCube.h"
#include <unordered_set>
using namespace std;

long long g1_state(FastCube cube)
{
    long long ans = 0;
    for (int i = 0; i < 12; i++)
    {
        ans |= (long long)cube.ops[i] << i;
    }
    return ans;
}

long long g2_state(FastCube cube)
{
    long long ans = 0;
    short i = 0;
    while (i < 12)
    {
        ans |= (long long)(cube.ps[i] / 4 == 0) << i;
        i += 1;
    }
    while (i < 20)
    {
        ans |= ((long long)cube.ops[i]) << (12 + 2 * (i - 12));
        i += 1;
    }
    return ans;
}

short C_OPPOSITES[8] = {14, 15, 12, 13, 18, 19, 16, 17};

long long g3_state(FastCube cube)
{
    long long ans = 0;
    short i = 0;
    long long e = 0;
    while (i < 12)
    {
        ans |= ((long long)(cube.ps[i] / 4)) << (2 * i);
        i += 1;
    }
    while (i < 20)
    {
        short a = (cube.ps[i] == i) || (cube.ps[i] == C_OPPOSITES[i - 12]);
        ans |= ((long long)((cube.ps[i] / 4) & 1) | (2 * a)) << (2 * i);
        e += cube.ps[i] == C_OPPOSITES[i - 12];
        i += 1;
    }
    ans |= (e % 4) << (2 * i);
    return ans;
}

long long g4_state(FastCube cube)
{
    long long ans = 0;
    for (int i = 0; i < 20; i++)
        ans |= ((long long)(cube.ps[i] == i)) << i;

    return ans;
}

vector<vector<short> > ALLOWED_MOVES;

void populate_allowed_moves()
{
    short arra[15] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    int n = sizeof(arra) / sizeof(arra[0]);
    vector<short> a(arra, arra + n);
    ALLOWED_MOVES.push_back(a);

    short arrb[15] = {0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrb) / sizeof(arrb[0]);
    vector<short> b(arrb, arrb + n);
    ALLOWED_MOVES.push_back(b);

    short arrc[15] = {0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrc) / sizeof(arrc[0]);
    vector<short> c(arrc, arrc + n);
    ALLOWED_MOVES.push_back(c);

    short arrd[12] = {0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrd) / sizeof(arrd[0]);
    vector<short> d(arrd, arrd + n);
    ALLOWED_MOVES.push_back(d);

    short arre[12] = {0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17};
    n = sizeof(arre) / sizeof(arre[0]);
    vector<short> e(arre, arre + n);
    ALLOWED_MOVES.push_back(e);

    short arrf[12] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
    n = sizeof(arrf) / sizeof(arrf[0]);
    vector<short> f(arrf, arrf + n);
    ALLOWED_MOVES.push_back(f);

    short arrg[18] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrg) / sizeof(arrg[0]);
    vector<short> g(arrg, arrg + n);
    ALLOWED_MOVES.push_back(g);
}

vector<vector<short> > REMOVE;

void populate_remove()
{
    short arra[4] = {0, 1, 15, 16};
    int n = sizeof(arra) / sizeof(arra[0]);
    vector<short> a(arra, arra + n);
    REMOVE.push_back(a);

    short arrb[4] = {3, 4, 9, 10};
    n = sizeof(arrb) / sizeof(arrb[0]);
    vector<short> b(arrb, arrb + n);
    REMOVE.push_back(b);

    short arrc[4] = {6, 7, 12, 13};
    n = sizeof(arrc) / sizeof(arrc[0]);
    vector<short> c(arrc, arrc + n);
    REMOVE.push_back(c);

    short arrd[0] = {};
    n = sizeof(arrd) / sizeof(arrd[0]);
    vector<short> d(arrd, arrd + n);
    REMOVE.push_back(d);
}

typedef long long (*state_fun)(FastCube cube);

state_fun CHECKS[4] = {g1_state, g2_state, g3_state, g4_state};

void clean_moves(short check)
{
    for (short remove : REMOVE[check])
    {
        for (int i = 0; i < 7; i++)
        {
            for (int j = 0; j < ALLOWED_MOVES[i].size(); j++)
            {
                if (ALLOWED_MOVES[i][j] == remove)
                {
                    ALLOWED_MOVES[i].erase(ALLOWED_MOVES[i].begin() + j);
                    break;
                }
            }
        }
    }
}

vector<short> phase_solve(FastCube &cube, FastCube goal, short check)
{
    vector<short> a;
    a.push_back(18);
    cube.scramble = a;
    vector<FastCube> states;
    states.push_back(cube);
    long long goal_state = CHECKS[check](goal);

    if (CHECKS[check](states[0]) == goal_state)
    {
        clean_moves(check);
        vector<short> ans;
        return ans;
    }

    while (true)
    {
        unordered_set<long long> seen;
        vector<FastCube> new_states;
        for (FastCube cube_state : states)
        {
            for (short move : ALLOWED_MOVES[cube_state.scramble[cube_state.scramble.size() - 1] / 3])
            {
                FastCube next_cube = cube_state;
                next_cube.move(move);
                long long next_state = CHECKS[check](next_cube);
                if (next_state == goal_state)
                {
                    vector<short> ans;
                    for (int i = 1; i < next_cube.scramble.size(); i++)
                    {
                        ans.push_back(next_cube.scramble[i]);
                    }
                    for (short turn : ans)
                    {
                        cube.move(turn);
                    }
                    clean_moves(check);
                    return ans;
                }
                if (seen.find(next_state) == seen.end())
                {
                    seen.insert(next_state);
                    new_states.push_back(next_cube);
                }
            }
        }
        states = new_states;
    }
}

vector<short> full_solve(FastCube cube)
{
    populate_allowed_moves();
    populate_remove();
    FastCube g;
    vector<short> ans;
    for (int i = 0; i < 4; i++)
    {
        vector<short> phase = phase_solve(cube, g, i);
        for (short num : phase)
            ans.push_back(num);
    }
    return ans;
}

/*
 * C++ implementation of Thistlethwaite's algorithm
 */

#include "FastCube.h"
#include <unordered_set>
#include <iostream>
using namespace std;

vector<vector<int> > ALLOWED_MOVES;

void populate_allowed_moves()
{
    int arra[15] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    int n = sizeof(arra) / sizeof(arra[0]);
    vector<int> a(arra, arra + n);
    ALLOWED_MOVES.push_back(a);

    int arrb[15] = {0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrb) / sizeof(arrb[0]);
    vector<int> b(arrb, arrb + n);
    ALLOWED_MOVES.push_back(b);

    int arrc[15] = {0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrc) / sizeof(arrc[0]);
    vector<int> c(arrc, arrc + n);
    ALLOWED_MOVES.push_back(c);

    int arrd[12] = {0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrd) / sizeof(arrd[0]);
    vector<int> d(arrd, arrd + n);
    ALLOWED_MOVES.push_back(d);

    int arre[12] = {0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17};
    n = sizeof(arre) / sizeof(arre[0]);
    vector<int> e(arre, arre + n);
    ALLOWED_MOVES.push_back(e);

    int arrf[12] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
    n = sizeof(arrf) / sizeof(arrf[0]);
    vector<int> f(arrf, arrf + n);
    ALLOWED_MOVES.push_back(f);

    int arrg[18] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
    n = sizeof(arrg) / sizeof(arrg[0]);
    vector<int> g(arrg, arrg + n);
    ALLOWED_MOVES.push_back(g);
}

vector<vector<int> > REMOVE;

void populate_remove()
{
    int arra[4] = {0, 1, 15, 16};
    int n = sizeof(arra) / sizeof(arra[0]);
    vector<int> a(arra, arra + n);
    REMOVE.push_back(a);

    int arrb[4] = {3, 4, 9, 10};
    n = sizeof(arrb) / sizeof(arrb[0]);
    vector<int> b(arrb, arrb + n);
    REMOVE.push_back(b);

    int arrc[4] = {6, 7, 12, 13};
    n = sizeof(arrc) / sizeof(arrc[0]);
    vector<int> c(arrc, arrc + n);
    REMOVE.push_back(c);

    int arrd[0] = {};
    n = sizeof(arrd) / sizeof(arrd[0]);
    vector<int> d(arrd, arrd + n);
    REMOVE.push_back(d);
}

void clean_moves(int check)
{
    for (int remove : REMOVE[check])
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

vector<int> g1_solve(FastCube &cube, FastCube goal)
{
    vector<int> a;
    a.push_back(18);
    cube.scramble = a;
    cube.set_phase(0);
    vector<FastCube> states;
    states.push_back(cube);
    int goal_state = goal.g1;

    if (cube.g1 == goal_state)
    {
        clean_moves(0);
        vector<int> ans;
        return ans;
    }

    while (true)
    {
        unordered_set<int> seen;
        vector<FastCube> new_states;
        for (FastCube cube_state : states)
        {
            int n = cube_state.scramble[cube_state.scramble.size() - 1] / 3;
            for (int move : ALLOWED_MOVES[n])
            {
                FastCube next_cube = cube_state;
                next_cube.move(move);
                int next_state = next_cube.g1;
                if (next_state == goal_state)
                {
                    vector<int> ans;
                    for (int i = 1; i < next_cube.scramble.size(); i++)
                    {
                        ans.push_back(next_cube.scramble[i]);
                    }
                    for (int turn : ans)
                    {
                        cube.move(turn);
                    }
                    clean_moves(0);
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

vector<int> g2_solve(FastCube &cube, FastCube goal)
{
    vector<int> a;
    a.push_back(18);
    cube.scramble = a;
    cube.set_phase(1);
    vector<FastCube> states;
    states.push_back(cube);
    int goal_state = goal.g2;

    if (cube.g2 == goal_state)
    {
        clean_moves(1);
        vector<int> ans;
        return ans;
    }

    while (true)
    {
        unordered_set<int> seen;
        vector<FastCube> new_states;
        for (FastCube cube_state : states)
        {
            int n = cube_state.scramble[cube_state.scramble.size() - 1] / 3;
            for (int move : ALLOWED_MOVES[n])
            {
                FastCube next_cube = cube_state;
                next_cube.move(move);
                int next_state = next_cube.g2;
                if (next_state == goal_state)
                {
                    vector<int> ans;
                    for (int i = 1; i < next_cube.scramble.size(); i++)
                    {
                        ans.push_back(next_cube.scramble[i]);
                    }
                    for (int turn : ans)
                    {
                        cube.move(turn);
                    }
                    clean_moves(1);
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

vector<int> g3_solve(FastCube &cube, FastCube goal)
{
    vector<int> a;
    a.push_back(18);
    cube.scramble = a;
    cube.set_phase(2);
    vector<FastCube> states;
    states.push_back(cube);
    long long goal_state = goal.g3;

    if (cube.g3 == goal_state)
    {
        clean_moves(2);
        vector<int> ans;
        return ans;
    }

    while (true)
    {
        unordered_set<long long> seen;
        vector<FastCube> new_states;
        for (FastCube cube_state : states)
        {
            int n = cube_state.scramble[cube_state.scramble.size() - 1] / 3;
            for (int move : ALLOWED_MOVES[n])
            {
                FastCube next_cube = cube_state;
                next_cube.move(move);
                long long next_state = next_cube.g3;
                if (next_state == goal_state)
                {
                    vector<int> ans;
                    for (int i = 1; i < next_cube.scramble.size(); i++)
                    {
                        ans.push_back(next_cube.scramble[i]);
                    }
                    for (int turn : ans)
                    {
                        cube.move(turn);
                    }
                    clean_moves(2);
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

vector<int> g4_solve(FastCube &cube, FastCube goal)
{
    vector<int> a;
    a.push_back(18);
    cube.scramble = a;
    cube.set_phase(3);
    vector<FastCube> states;
    states.push_back(cube);
    int goal_state = goal.g4;

    if (cube.g4 == goal_state)
    {
        clean_moves(3);
        vector<int> ans;
        return ans;
    }

    while (true)
    {
        unordered_set<int> seen;
        vector<FastCube> new_states;
        for (FastCube cube_state : states)
        {
            int n = cube_state.scramble[cube_state.scramble.size() - 1] / 3;
            for (int move : ALLOWED_MOVES[n])
            {
                FastCube next_cube = cube_state;
                next_cube.move(move);
                int next_state = next_cube.g4;
                if (next_state == goal_state)
                {
                    vector<int> ans;
                    for (int i = 1; i < next_cube.scramble.size(); i++)
                    {
                        ans.push_back(next_cube.scramble[i]);
                    }
                    for (int turn : ans)
                    {
                        cube.move(turn);
                    }
                    clean_moves(3);
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

vector<int> full_solve(FastCube cube)
{
    populate_allowed_moves();
    populate_remove();
    FastCube g;
    vector<int> ans;
    vector<int> phase1 = g1_solve(cube, g);
    for (int num : phase1)
        ans.push_back(num);
    // cout << "g1 done" << endl;

    vector<int> phase2 = g2_solve(cube, g);
    for (int num : phase2)
        ans.push_back(num);
    // cout << "g2 done" << endl;

    vector<int> phase3 = g3_solve(cube, g);
    for (int num : phase3)
        ans.push_back(num);
    // cout << "g3 done" << endl;

    vector<int> phase4 = g4_solve(cube, g);
    for (int num : phase4)
        ans.push_back(num);
    // cout << "g4 done" << endl;

    return ans;
}

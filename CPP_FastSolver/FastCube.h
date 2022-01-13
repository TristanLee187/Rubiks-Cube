/*
 * C++ implementation of the FastCube object, with modifications for performance.
 * Rather than keeping track of piece locations and orientations and then calculating
 * G1 through G4 states after each move, we can keep track of the states instead 
 * and have each move affect the states directly.
 */

#include <vector>
#include <string>
using namespace std;

int E_MOVES[18][4] = {
    {0, 5, 1, 4}, {4, 1, 5, 0}, {0, 5, 1, 4}, {1, 9, 2, 10}, {10, 2, 9, 1}, {1, 9, 2, 10}, {5, 8, 6, 9}, {9, 6, 8, 5}, {5, 8, 6, 9}, {0, 11, 3, 8}, {8, 3, 11, 0}, {0, 11, 3, 8}, {4, 10, 7, 11}, {11, 7, 10, 4}, {4, 10, 7, 11}, {2, 6, 3, 7}, {7, 3, 6, 2}, {2, 6, 3, 7}};

int C_MOVES[18][4] = {
    {12, 13, 14, 15}, {15, 14, 13, 12}, {12, 13, 14, 15}, {15, 14, 18, 19}, {19, 18, 14, 15}, {15, 14, 18, 19}, {14, 13, 17, 18}, {18, 17, 13, 14}, {14, 13, 17, 18}, {13, 12, 16, 17}, {17, 16, 12, 13}, {13, 12, 16, 17}, {12, 15, 19, 16}, {16, 19, 15, 12}, {12, 15, 19, 16}, {19, 18, 17, 16}, {16, 17, 18, 19}, {19, 18, 17, 16}};

int G2_C_MOVES[18][4] = {
    {12, 14, 16, 18}, {18, 16, 14, 12}, {12, 14, 16, 18}, {18, 16, 24, 26}, {26, 24, 16, 18}, {18, 16, 24, 26}, {16, 14, 22, 24}, {24, 22, 14, 16}, {16, 14, 22, 24}, {14, 12, 20, 22}, {22, 20, 12, 14}, {14, 12, 20, 22}, {12, 18, 26, 20}, {20, 26, 18, 12}, {12, 18, 26, 20}, {26, 24, 22, 20}, {20, 22, 24, 26}, {26, 24, 22, 20}};

int CO[] = {1, 2, 0, 2, 0, 1};

int C_OPPOSITES[] = {14, 15, 12, 13, 18, 19, 16, 17};

void rotate(vector<int> &a, int b[][4], int c, int offset)
{
    int w = a[b[c][(offset == 2) ? 2 : 3]];
    int x = a[b[c][(offset == 2) ? 3 : 0]];
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
    vector<int> scramble;
    int g1;
    int g2;
    long long g3;
    int g4;
    int phase;

    FastCube()
    {
        for (int i = 0; i < 20; i++)
        {
            ps.push_back(i);
        }
        g1 = 0;
        g2 = 15;
        g3 = 734433793280;
        g4 = 1048575;
        phase = 0;
    }

    FastCube(string layout)
    {
        vector<string> layout_vector = split(layout);
        for (int i = 0; i < 20; i++)
        {
            ps.push_back(stoi(layout_vector[i]));
        }
        g1 = stoi(layout_vector[20]);
        g2 = stoi(layout_vector[21]);
        g3 = stoll(layout_vector[22]);
        g4 = stoi(layout_vector[23]);
    }

    void g1_rotate(int turn, int offset)
    {
        int a = E_MOVES[turn][0];
        int b = E_MOVES[turn][1];
        int c = E_MOVES[turn][2];
        int d = E_MOVES[turn][3];
        int e = offset & 1;
        int or_change = (((turn / 3) == 0) | ((turn / 3) == 5)) & e;
        int ba = ((g1 & (1 << a)) >> a) ^ or_change;
        int bb = ((g1 & (1 << b)) >> b) ^ or_change;
        int bc = ((g1 & (1 << c)) >> c) ^ or_change;
        int bd = ((g1 & (1 << d)) >> d) ^ or_change;

        g1 &= ((1 << 12) - 1) ^ ((1 << a) | (1 << b) | (1 << c) | (1 << d));
        g1 |= (ba << (e ? b : c)) | (bb << (e ? c : d)) | (bc << (e ? d : a)) | (bd << (e ? a : b));
    }

    void g2_rotate(int turn, int offset)
    {
        // edges
        int a = E_MOVES[turn][0];
        int b = E_MOVES[turn][1];
        int c = E_MOVES[turn][2];
        int d = E_MOVES[turn][3];
        int e = offset & 1;
        int ba = ((g2 & (1 << a)) >> a);
        int bb = ((g2 & (1 << b)) >> b);
        int bc = ((g2 & (1 << c)) >> c);
        int bd = ((g2 & (1 << d)) >> d);

        g2 &= ((1 << 28) - 1) ^ ((1 << a) | (1 << b) | (1 << c) | (1 << d));
        g2 |= (ba << (e ? b : c)) | (bb << (e ? c : d)) | (bc << (e ? d : a)) | (bd << (e ? a : b));

        // corners
        a = G2_C_MOVES[turn][0];
        b = G2_C_MOVES[turn][1];
        c = G2_C_MOVES[turn][2];
        d = G2_C_MOVES[turn][3];
        ba = (g2 & (3 << a)) >> a;
        bb = (g2 & (3 << b)) >> b;
        bc = (g2 & (3 << c)) >> c;
        bd = (g2 & (3 << d)) >> d;

        if (e)
        {
            ba = ((ba << 1) + CO[turn / 3]) % 3;
            bb = ((bb << 1) + CO[turn / 3]) % 3;
            bc = ((bc << 1) + CO[turn / 3]) % 3;
            bd = ((bd << 1) + CO[turn / 3]) % 3;
        }

        g2 &= ((1 << 28) - 1) ^ ((3 << a) | (3 << b) | (3 << c) | (3 << d));
        g2 |= (ba << (e ? b : c)) | (bb << (e ? c : d)) | (bc << (e ? d : a)) | (bd << (e ? a : b));
    }

    void g3_rotate(int turn, int offset)
    {
        // edges
        int a = E_MOVES[turn][0] << 1;
        int b = E_MOVES[turn][1] << 1;
        int c = E_MOVES[turn][2] << 1;
        int d = E_MOVES[turn][3] << 1;
        int e = offset & 1;
        long long ba = (g3 & (3 << a)) >> a;
        long long bb = (g3 & (3 << b)) >> b;
        long long bc = (g3 & (3 << c)) >> c;
        long long bd = (g3 & (3 << d)) >> d;
        g3 &= (((long long)1 << 42) - 1) ^ (((long long)3 << a) | ((long long)3 << b) | ((long long)3 << c) | ((long long)3 << d));
        g3 |= (ba << (e ? b : c)) | (bb << (e ? c : d)) | (bc << (e ? d : a)) | (bd << (e ? a : b));

        // corners
        a = C_MOVES[turn][0];
        b = C_MOVES[turn][1];
        c = C_MOVES[turn][2];
        d = C_MOVES[turn][3];
        int d_a = (ps[a] == a | ps[a] == C_OPPOSITES[a - 12]) << 1;
        int d_b = (ps[b] == b | ps[b] == C_OPPOSITES[b - 12]) << 1;
        int d_c = (ps[c] == c | ps[c] == C_OPPOSITES[c - 12]) << 1;
        int d_d = (ps[d] == d | ps[d] == C_OPPOSITES[d - 12]) << 1;
        ba = ((ps[a] >> 2) & 1) | d_a;
        bb = ((ps[b] >> 2) & 1) | d_b;
        bc = ((ps[c] >> 2) & 1) | d_c;
        bd = ((ps[d] >> 2) & 1) | d_d;
        g3 &= (((long long)1 << 42) - 1) ^ (((long long)3 << 40) | ((long long)3 << (a << 1)) | ((long long)3 << (b << 1)) | ((long long)3 << (c << 1)) | ((long long)3 << (d << 1)));
        g3 |= (ba << (a << 1)) | (bb << (b << 1)) | (bc << (c << 1)) | (bd << (d << 1));

        // opposite corner count
        e = 0;
        for (int i = 12; i < 20; i++)
        {
            e += ps[i] == C_OPPOSITES[i - 12];
        }
        g3 |= (long long)(e % 4) << 40;
    }

    void g4_rotate(int turn, int offset)
    {
        int ans = 0;
        for (int i = 0; i < 20; i++)
        {
            ans |= (ps[i] == i) << i;
        }
        g4 = ans;
    }

    long long g3_state()
    {
        long long ans = 0;
        int i = 0;
        int e = 0;
        while (i < 12)
        {
            ans |= ((long long)(ps[i] / 4)) << (2 * i);
            i += 1;
        }
        while (i < 20)
        {
            int a = ((ps[i] == i) || (ps[i] == C_OPPOSITES[i - 12])) ? 2 : 0;
            ans |= ((long long)((ps[i] / 4) & 1) | a) << (2 * i);
            e += (ps[i] == C_OPPOSITES[i - 12]) ? 1 : 0;
            i += 1;
        }
        ans |= ((long long)(e % 4)) << (2 * i);
        return ans;
    }

    int g4_state()
    {
        int ans = 0;
        for (int i = 0; i < 20; i++)
            ans |= (((ps[i] == i) ? 1 : 0)) << i;

        return ans;
    }

    void move(int turn)
    {
        int offset = ((turn % 3) >> 1) + 1;
        rotate(ps, E_MOVES, turn, offset);
        rotate(ps, C_MOVES, turn, offset);
        if (phase == 0)
        {
            g1_rotate(turn, offset);
            g2_rotate(turn, offset);
        }
        else if (phase == 1)
            g2_rotate(turn, offset);
        else if (phase == 2)
            g3_rotate(turn, offset);
        else
            g4_rotate(turn, offset);
        scramble.push_back(turn);
    }

    void set_phase(int p)
    {
        phase = p;
        if (phase == 2)
            g3 = g3_state();
        if (phase == 3)
            g4 = g4_state();
    }
};

/*
 * Main C++ file to be compiled and then run outside the CPP_FastSolver folder.
 * Compiled using the -Ofast optimization flag to produce solver.out.
 * 
 * Takes as input on the command line the 54 stickers of a cube, in standard
 * orientation, from left to right and top to bottom, separated by spaces.
 * 
 * Passes these stickers to convert.py (using a subprocess) to generate the piece
 * vector and G1 through G4 states of the FastCube object.
 * 
 * Creates a FastCube from these values, and calls FullSolve on it.
 * 
 * Prints the found solution to standard output.
 */

#include "FullSolve.h"
#include <stdlib.h>
#include <iostream>
#include <stdio.h>

using namespace std;

string exec(string command)
{
    char buffer[128];
    string result = "";

    // Open pipe to file
    FILE *pipe = popen(command.c_str(), "r");
    if (!pipe)
    {
        return "popen failed!";
    }

    // read till end of process:
    while (!feof(pipe))
    {

        // use buffer to read and add to result
        if (fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }

    pclose(pipe);
    return result;
}

vector<string> scramble_num_to_str(vector<int> scramble)
{
    vector<string> ans;
    string moves[] = {"U", "F", "R", "B", "L", "D"};
    string adds[] = {"", "\'", "2"};
    for (int num : scramble)
    {
        ans.push_back(moves[num / 3] + adds[num % 3]);
    }
    return ans;
}

int main(int argc, char **argv)
{
    vector<string> layout;
    for (int i = 1; i < 55; i++)
    {
        layout.push_back(argv[i]);
    }
    string layout_string = "";
    for (string s : layout)
        layout_string += s + " ";

    string cube_str = exec("pypy3 CPP_FastSolver/convert.py " + layout_string);

    FastCube cube(cube_str);
    vector<int> sol;
    sol = full_solve(cube);
    vector<string> solution;
    solution = scramble_num_to_str(sol);
    for (string move : solution)
    {
        cout << move << " ";
    }
    cout << endl;

    return 0;
}

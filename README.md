# Rubik's Cube
3 Interactive Rubik's Cube programs and a solver implementing a slightly modified Thistlethwaite's Algorithm, written in Python and C++.


## Requirements
* The terminal based script requires just base Python3.

* The 2D rendering program requires PyGame, which can be installed with `pip`: `pip install pygame`.

* The 3D rendering program requires both PyGame and PyOpenGL, the latter of which can also be installed with `pip`: `pip install PyOpenGL`.
    * For Mac users first using PyOpenGL, you may encounter a common ImportError; [here](https://github.com/PixarAnimationStudios/USD/issues/1372) is a solution to it.

* All 3 programs use the same solver, which requires an at least C++11 compiler.


## Usage
### Starting each program
For users with Make installed:

* `make build` must be executed first to use any solver functionality; it compiles the C++ file containing the solver.

* `make help` details how to start each of the programs, also detailed below.

* `make interact` starts the terminal based script.

* `make app` starts the PyGame based, 2D and isometric projection program.

* `make 3D` starts the PyGame wrapped, PyOpenGL 3D rendering program.

For users without Make:

The solver executable file requires just one compilation. Using `clang++` from the Rubiks-Cube directory: 
`clang++ CPP_FastSolver/solver.cpp -o CPP_FastSolver/solver.out -Ofast`.

Each program can be run with just `python3` from the terminal:

* `python3 interact.py` starts the terminal based script.

* `python3 app.py` starts the PyGame based, 2D and isometric projection program.

* `python3 3D.py` starts the PyGame wrapped, PyOpenGL 3D rendering program.

### Usage within each program
#### Terminal based script
This script uses a command-line style UI, with the following commands:

* `help` prints the help menu (the text below) to standard output.

* `scramble` followed by moves in cube notation (`R, L, R', R2,` etc.) will scramble the cube accordingly; you can put 
multiple moves on the same line, separated by spaces. Supported moves include: the outer face turns (`R, L, U, D, F, B`), 
their corresponding wide moves (`r, l, u, d, f, b`), slice moves (`M, E, S`), and cube rotations (`x, y, z`).

* `random n` applies a random scramble of length n to the cube, and prints the scramble to standard output.

* `read filename` reads a scramble in cube notation from filename (a text file), and applies the scramble to the cube 
(see scramble.txt for an example).

* `see filename` gets the colors of the stickers of each face of the cube in a flat format from filename (a text file), 
and assigns those colors to the cube (see layout.txt for an example).

* `reset` replaces the cube with a new (solved) cube object.

* `solve` uses the solver executable in the CPP_FastSolver package to get a solution to the scrambled cube, prints it, and applies it to the cube.

* `print` prints the cube in a flat layout.

* `quit` stops the interactive script.

#### 2D PyGame Program
This program uses PyGame to run a button based GUI:

* Clicking the `?` button brings up the help menu (the text below) in a PyGame window that replaces the previous one; 
closing the help window brings back the previous PyGame window.
  
* Clicking one of the buttons with cube notation moves performs the corresponding move.

    * Holding `Shift` while pressing one of these buttons performs the counterclockwise counterpart.
    
    * Using right click has the same effect.
    
    * Doing both of these simultaneously does the clockwise move (same as a regular button press).
    
* Clicking `Reset` returns the cube to the solved state and standard orientation (white on top, green in front).

* Clicking `Scramble` applies a random, 20 move scramble to the cube, and prints the scramble to standard output.

* Clicking `Solve` gets a solution to the scrambled cube, prints it to standard output, and applies it to the cube.

* Clicking `Switch` switches the viewing layout of the cube; if you`re viewing it in a flat layout, the view changes to 
an isometric projection, and vice versa.

    * For the flat layout, the top and bottom faces of the cube are in their respective places; the faces in the middle, 
from left to right, are the cube`s left, front, right, and back faces.
    
    * For the isometric layout, the left, top, and right faces are the cube`s front, top, and right faces.
    
#### 3D PyGame and PyOpenGL program
This program uses PyOpenGL to render a cube object in 3D, and wraps that rendering with PyGame.

* Pressing the `r`, `l`, `u`, `d`, `f`, or `b` keys performs the corresponding outer face turn.

* Pressing the `x` or `y` keys rotates the cube about the x or y axes.
    
* Holding `Shift` while pressing any of the above keys performs the counterclockwise counterpart.

* Clicking and dragging with the mouse also rotates the cube.

* Pressing the `s` key applies a random 20 move scramble to the cube.

* Pressing the space bar gets a solution to the scrambled cube, prints it to standard output, and applies it to the cube.

## Notes on the Solver

### My solver implements a slightly modified version of Thistlethwaite's Algorithm to solve the cube. Thistlethwaite's Algorithm without any modification is detailed below.

At a high level, the algorithm works by progressing through 4 stages. The cube must meet certain requirements to reach
each stage; once a stage is met, some moves are removed from the set of moves needed to solve the cube, such that the requirements of one stage carry over into the next.

For example, the first stage consists of the set of any state of the cube (G<sub>0</sub>), and the set of moves needed 
to reach the second stage (all 18 moves). For a cube to meet the requirements of the second stage, all the edges must be oriented
such that they can be placed in their correct location in the correct orientation without quarter turns of the U and D
face. Once this stage is reached, quarter turns of the U and D faces are removed from the set of allowed moves; now,
when progressing to the third stage, all possible cube states will also meet the requirements of the second stage.
Notice that any state in G<sub>i+1</sub> is also in G<sub>i</sub>; i.e., the set of states in G<sub>i+1</sub> is a subset 
of the states in G<sub>i</sub>, for appropriate values of i. Progression is made in this manner until the fifth stage is 
reached; only one state meets the requirements for this stage: the solved state.

We progress through the stages with iterative deepening depth first search (IDDFS). We start at depth 0. For any depth
*d*, we generate all combinations of moves of length *d* given the allowed moves of the current stage. If one of these
combinations moves the cube into the next stage, then we add it to the solution, and move on to the next stage,
removing moves from the set of allowed moves as appropriate.  
If none of the combinations work, then we increase the depth by 1 and generate all combinations of that length, check
those, and so on. This incrementing of the depth ensures that the solution between stages is always of the shortest
possible length.

Below are the details for each stage:

* G<sub>0</sub> &rarr; G<sub>1</sub>
  * All 18 moves are allowed.
  * G<sub>1</sub> requirement: all edges must be "good", or able to be solved without 90 degree turns of the U or D face.

* G<sub>1</sub> &rarr; G<sub>2</sub>
  * All moves besides `U`, `U'`, `D`, or `D'` are allowed, which makes for `U2, F, F', F2, R, R', R2, B, B', B2, L, L', L2, D2`.
  * G<sub>2</sub> requirement: all corners are oriented correctly (left or right sticker must point left or right), and edges in 
the M slice must all belong in the M slice.

* G<sub>2</sub> &rarr; G<sub>3</sub> 
  * All moves from G<sub>1</sub> &rarr; G<sub>2</sub> are allowed besides `F`, `F'`, `B`, and `B'`, which makes for `U2, F2, R, R', R2, B2, L, L', L2, 
D2`.
  * G<sub>3</sub> requirement: all edges must be in their home slice (E or S slice), all corners must be positionsed such that all stickers on any 1 of the 6 faces of the cube contain are either the correct color or opposite the correct color.

* G<sub>3</sub> &rarr; G<sub>4</sub>
  * Allowed moves: `U2, F2, R2, B2, L2, D2`.
  * G<sub>4</sub> requirement: all pieces are in their correct location.

The algorithm that I implement differs slightly from Thistlethwaite's Algorithm, specifically in the G<sub>3</sub> stage. My third stage is detailed below:

* G<sub>2</sub> &rarr; G<sub>3</sub> 
  * All moves from G<sub>1</sub> &rarr; G<sub>2</sub> are allowed besides `F`, `F'`, `B`, and `B'`, which makes for `U2, F2, R, R', R2, B2, L, L', L2, 
D2`.
  * G<sub>3</sub> requirement: all edges must be in their home slice (E or S slice), all corners must be in their home slice (U or D face), and the number of corners opposite their correct location must be equal to 0 module 4.

My third stage has a stricter requirement than that of Thistlethwaite's Algorithm: the set of all cube states that follow my third stage requirement is a proper subset of G<sub>3</sub>. This should theoretically lead to larger move counts in the solution, but in my tests the solution lengths are very comparable. I chose to use this different third stage because it was both easier to implement in code and ran slightly faster.


### Implementation Notes

The `Rubiks-Cube` directory contains directories `Solver` (a Python solver used in previous versions of this project) and
`CPP_FastSolver` (the C++ compiled executable solver now used in all the programs). While both implement 
Thistlethwaite's Algorithm, there are implementation differences in the data structure used to represent a cube 
(that do in fact make the C++ implementation faster).

#### Common to both solvers
I use pruning to eliminate branches of this tree (which is very helpful considering branching factors of around 15). 
Though two different scrambles will very likely produce two different states, each stage
considers only certain details about the current state to be important, based on its requirements. For example, the
second stage only cares about the orientation of the edge pieces. Therefore, this stage considers two states with
the same orientation of edges at each location on the cube to be the same, even if the actual edge pieces at those
locations are different, all regardless of any information about the corner pieces. This pruning reduces the maximum
possible runtime from the order of trillions to just over one million (see https://www.jaapsch.net/puzzles/thistle.htm
for these factors, as well as an overview of the algorithm from Thistlethwaite's papers). With pruning, the algorithm 
resembles Breadth First Search (BFS) more than IDDFS. 

Programmatically, arrays of values can capture information of each G1 through G4 state, but I use integers and bitwise 
operations to increase speed; at most, these integers can reach values around 2<sup>42</sup>, which is handled without 
issue in Python and requires the `long long` data type in C++.

My implementation minds symmetry of turning faces along the same axis.
For example, applying a U face turn (`U`, `U'`, or `U2`) twice in a row can be captured by a single U face turn, so this
should not be allowed. Also, applying a U move and then a D move has the same effect as applying the D move first then
the U move, so only one of these should be allowed.

Finally, I implement a function to simplify a solution to possibly decrease the move count if certain adjacent moves in
the solution rotate along the same axis. For example, the scramble `U U2` is equivalent to just `U'`, and `R L R` is 
equivalent to `R2 L`.

#### Differences between the solvers

The Python and C++ solvers differ mainly in what information their cube data structure (called FastCube) holds, and 
therefore what steps must be performed when manipulating and comparing cube states.

The Python solver's FastCube uses two arrays to hold the locations of each piece and their orientations. Cube moves
manipulate these arrays. When solving, external functions compute the states from the cube's piece and orientation 
arrays. It's a more straightforward application of the requirements of each stage.

What the C++ solver's FastCube does differently is keep track of its own states. Moves affect these states directly,
rather than having functions evaluate them externally. This results in faster times for a few reasons:
* An orientation array is not needed; all the information needed about orientations are captured in the states, which
take up less space and are faster to copy than arrays (a piece location array is still needed, though). This also 
eliminates an intermediate step to getting the states.
* The internal functions that change states directly should be faster than the external ones on average: they mostly 
perform bitwise operations, which are faster than external array accessing.

#### Performance
Running solver_comparison.py in the Rubiks-Cube directory, run with `pypy3 solver_comparison.py` followed by a single 
integer n, generates n random scrambles and compares the Python and C++ times and solutions. Note that I run the Python
solver with PyPy, a faster implementation of Python. If regular Python was used, average times would be at least several
minutes. Also note that both implementations should produce the same solutions to the same scrambles, so the average
solution lengths should be the same.

I arrived at the following statistics running `pypy3 solver_comparison.py 100` on my laptop with a 1.6 Ghz processor:
* Average solution length: 31.74
* Average PyPy solve time: 16.54 seconds
* Average C++ solve time: 12.05 seconds

I also observed the general memory usage for each solver using Activity Monitor:
* Average PyPy memory usage: 1-1.5 GB
* Average C++ memory usage: 400-750 MB

Very roughly, the C++ solver uses 25% less time and 50% less memory.

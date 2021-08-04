# Rubik's Cube
3 Interactive Rubik's Cube programs and a solver implementing Thistlethwaite's Algorithm, all written in Python


## Requirements
* The terminal based script requires just base Python3

* The 2D rendering program requires PyGame, which can be installed with `pip`: `pip install pygame`

* The 3D rendering program requires both PyGame and PyOpenGL, the latter of which can also be installed with `pip`: `pip install PyOpenGL`
    * For Mac users first using PyOpenGL, you may encounter a common ImportError; [here](https://github.com/PixarAnimationStudios/USD/issues/1372) is a solution to it

* In all 3 programs, the solver requires PyPy3, which can be installed with `brew`: `brew install pypy3`


## Usage
### Starting each program
For users with Make installed:

* `make help` details how to start each of the programs, also detailed below

* `make interact` starts the terminal based script

* `make app` starts the PyGame based, 2D and isometric projection program

* `make 3D` starts the PyGame wrapped, PyOpenGL 3D rendering program

For users without Make, each program can also be run with just `python3` from the terminal:

* `python3 interact.py` starts the terminal based script

* `python3 app.py` starts the PyGame based, 2D and isometric projection program

* `python3 3D.py` starts the PyGame wrapped, PyOpenGL 3D rendering program

### Usage within each program
#### Terminal based script
This script uses a command-line style UI, with the following commands:

* `help` prints the help menu (the text below) to standard output

* `scramble` followed by moves in cube notation (R, L, R', R2, etc.) will scramble the cube accordingly; you can put multiple moves on the same line, separated by spaces. Supported moves include: the outer face turns (R, L, U, D, F, B), their corresponding wide moves (r, l, u, d, f, b), slice moves (M, E, S), and cube rotations (x, y, z)

* `random n` applies a random scramble of length n to the cube, and prints the scramble to standard output

* `read filename` reads a scramble in cube notation from filename (a text file),
        and applies the scramble to the cube (see scramble.txt for an example)

* `see filename` gets the colors of the stickers of each face of the cube in a flat format
        from filename (a text file), and assigns those colors to the cube (see layout.txt for an example)

* `reset` replaces the cube with a new (solved) cube object

* `solve` uses the solver in the Solver package to get a solution to the scrambled cube, and prints it

* `print` prints the cube in a flat layout

* `quit` stops the interactive script

#### 2D PyGame Program
This program uses PyGame to run a button based GUI:

* Clicking the '?' button brings up the help menu (the text below) in a PyGame window that replaces the previous one; closing the help window brings back the old one
  
* Clicking one of the buttons with cube notation moves performs the corresponding move

    * Holding `Shift` while pressing one of these buttons performs the counterclockwise counterpart
    
    * Using right click has the same effect
    
    * Doing both of these simultaneously does the clockwise move (same as a regular button press)
    
* Clicking 'Reset' returns the cube to the solved state and standard orientation (white on top, green in front)

* Clicking 'Scramble' applies a random, 20 move scramble to the cube, and prints the scramble to standard output

* Clicking 'Solve' gets a solution to the scrambled cube, prints it to standard output, and applies it to the cube

* Clicking 'Switch' switches the viewing layout of the cube; if you`re viewing it in a flat layout, the view changes to an isometric projection, and vice versa

    * For the flat layout, the top and bottom faces of the cube are in their respective places; the faces in the middle, from left to right, are the cube`s left, front, right, and back faces
    
    * For the isometric layout, the left, top, and right faces are the cube`s front, top, and right faces
    
#### 3D PyGame and PyOpenGL program
This program uses PyOpenGL to render a cube object in 3D, and wraps that rendering with PyGame

* Pressing the `r`, `l`, `u`, `d`, `f`, or `b` keys performs the corresponding outer face turn

* Pressing the `x` or `y` keys rotates the cube about the x or y axes
    
* Holding `Shift` while pressing any of the above keys performs the counterclockwise counterpart

* Clicking and dragging with the mouse also rotates the cube

* Pressing the space bar gets a solution to the scrambled cube, prints it to standard output, and applies it to the cube

## Notes on the Solver

####My solver implements Thistlethwaite's Algorithm to solve the cube, detailed below.

At a high level, the algorithm works by progressing through 4 stages. The cube must meet certain requirements to reach
each stage; once a stage is met, some moves are removed from the set of moves needed to solve the cube, such that the
requirements of one stage carry over into the next.

For example, the first stage consists of the set of any state of the cube (G0), and the set of moves needed to reach the
second stage (all 18 moves). For a cube to meet the requirements of the second stage, all the edges must be oriented
such that they can be placed in their correct location in the correct orientation without quarter turns of the U and D
face. Once this stage is reached, quarter turns of the U and D faces are removed from the set of allowed moves; now,
when progressing to the third stage, all possible cube states will also meet the requirements of the second stage.
Notice that any state in group i+1 is also in group i; i.e., the set of states in group i+1 is a subset of the states
in group i. Progression is made in this manner until the fifth stage is reached; only one state meets the
requirements for this stage: the solved state. See the corresponding files for details on each stage.

We progress through the stages with iterative deepening depth first search (IDDFS). We start at depth 0. For any depth
d, we generate all combinations of moves of length d given the allowed moves of the current stage. If one of these
combinations moves the cube into the next stage, then we add it to the solution, and move on to the next stage,
removing moves from the set of allowed moves as appropriate.
If none of the combinations work, then we increase the depth by 1 and generate all combinations of that length, check
those, and so on. This incrementing of the depth ensures that the solution between stages is always of the shortest
possible length. The scramble field of each FastCube object keeps track of the moves applied to each instance.
A note about generating combinations of moves: my implementation minds symmetry of turning faces along the same axis.
For example, applying a U face turn (U, U', or U2) twice in a row can be captured by a single U face turn, so this
should not be allowed. Also, applying a U move and then a D move has the same effect as applying the D move first then
the U move, so only one of these should be allowed.

At a lower level, I also use pruning to eliminate branches of this tree (which is very helpful considering branching
factors of around 15). Though two different scrambles will very likely produce two different states, each stage
considers only certain details about the current state to be important, based on its requirements. For example, the
second stage only cares about the orientation of the edge pieces. Therefore, this stage considers two states with
the same orientation of edges at each location on the cube to be the same, even if the actual edge pieces at those
locations are different, all regardless of any information about the corner pieces. This pruning reduces the maximum
possible runtime from the order of trillions to just over one million (see https://www.jaapsch.net/puzzles/thistle.htm
for these factors, as well as an overview of the algorithm from Thistlethwaite's papers). Programmatically, arrays of
values can capture this information, but I use integers and bitwise operations to increase speed; at most, these
integers can reach values around 2^42, which Python handles without issue.

Finally, I implement a function to simplify a solution to decrease the move count. For example, the scramble 'U U2' is
equivalent to just 'U'', and 'R L R' is equivalent to 'R2 L'.

####Performance
Using the mass testing functionality of tester.py in the Solver package (run with `pypy3 tester.py Tests 100`) multiple
times, I arrived at the following per-solve statistics:

Average time to solve: 12-14 seconds

Average length of solution: 32-35 moves

Average RAM usage: 1.5-2 GB
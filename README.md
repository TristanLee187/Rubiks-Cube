# Rubik's Cube
3 Interactive Rubik's Cube programs, written in Python


## Requirements
* The terminal based script only requires base Python3

* The 2D rendering program requires PyGame, which can be installed with pip: `pip install pygame`

* The 3D rendering program requires both PyGame and PyOpenGL, that latter of which can also be installed with pip: `pip install PyOpenGL`
    * For Mac users first using PyOpenGL, you may encounter a common ImportError; [here](https://github.com/PixarAnimationStudios/USD/issues/1372) is a solution to it
    
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

* Pressing 'Switch' switches the viewing layout of the cube; if you`re viewing it in a flat layout, the view changes to an isometric projection, and vice versa

    * For the flat layout, the top and bottom faces of the cube are in their respective places; the faces in the middle, from left to right, are the cube`s left, front, right, and back faces
    
    * For the isometric layout, the left, top, and right faces are the cube`s front, top, and right faces
    
#### 3D PyGame and PyOpenGL program (in progress)
This program uses PyOpenGL to render a cube object in 3D, and wraps that rendering with PyGame

* Pressing the `r`, `l`, `u`, `d`, `f`, or `b` keys performs the corresponding outer face turn

* Pressing the `x` or `y` keys rotates the cube about the x or y axes
    
* Holding `Shift` while pressing any of the above keys performs the counterclockwise counterpart

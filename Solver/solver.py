# Main solver file to be run outside the package

from FastCube import FastCube
from FullSolve import full_solve
from sys import argv

if __name__ == '__main__':
    cube = FastCube(argv[1])

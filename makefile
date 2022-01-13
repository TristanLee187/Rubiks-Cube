interact:
	@python3 interact.py

app:
	@python3 app.py

help:
	@cat make_help.txt

3D:
	@python3 3D.py

build:
	@clang++ CPP_FastSolver/solver.cpp -o CPP_FastSolver/solver.out -Ofast
import subprocess
import shutil
import random
import numpy as np
from tqdm import tqdm

# Helper function to generate unique coordinates
def gencoordinates(n):
    seen = set()

    x, y = random.randint(0, n), random.randint(0, n)

    while True:
        seen.add((x, y))
        yield (x, y)
        x, y = random.randint(0, n), random.randint(0, n)
        while (x, y) in seen:
            x, y = random.randint(0, n), random.randint(0, n)

# Parameters of puzzle
N = 5
N_GAMES = 10000
N_COLORS = 3
COLORS = ["R", "G", "B", "Y", "O"]
color_choices = COLORS[:N_COLORS]

for i in tqdm(range(N_GAMES)):
    # Generate blank puzzle
    puzzle = np.zeros((N,N), 'U1')
    puzzle.fill('.')

    # Fill puzzle with colors.
    coords = gencoordinates(N-1)
    for color in color_choices:
        for j in range(2):
            x,y = next(coords)
            puzzle[x,y] = color
        
    # Format puzzle for solver
    with open("test_puzzle.txt", 'w') as puzzle_file:
        for row in puzzle:
            puzzle_file.write("".join(row))
            puzzle_file.write("\n")

    solution = subprocess.run(["python", "pyflowsolver.py", "test_puzzle.txt"], stdout=subprocess.PIPE)
    result = solution.stdout.decode('utf-8')

    if 'UNSAT' in result:
        continue
    else:
        output_file = f'solvable\\random_{N}x{N}_{i}.txt'
        shutil.copyfile("test_puzzle.txt", output_file)
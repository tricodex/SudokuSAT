from sympy.logic.utilities.dimacs import load_file
from os.path import join
import math

sudoku_rules_path = "../input"

sudoku_rules = {
    4 : "sudoku-rules-4x4.txt",
    9 : "sudoku-rules-9x9.txt",
   16 : "sudoku-rules-16x16.txt"
}

# Converts one line of dot format (one puzzle) into DIMACS
def get_dimacs_string(line):
    sudoku_string = ""
    cnt = 3
    for tok in line:
        cnt += 1
        if tok.isnumeric():
            sudoku_string += str(cnt // math.isqrt(len(line)))
            sudoku_string += str(cnt % math.isqrt(len(line))+1)
            sudoku_string += tok
            sudoku_string += " 0/n"
    return sudoku_string


# Gets the SUDOKU rules corresponding to the size as CNF clause
def get_sudoku_rules_dimacs(sudoku_size):
    return load_file(join(sudoku_rules_path, sudoku_rules[sudoku_size]))

# Gets the puzzles from the file as SAT CNF clauses
def parse_puzzles(puzzles_file):
    puzzles = []
    for line in puzzles_file.readline():
        puzzle_size = sqrt(len(line))
        puzzle.append(load(get_dimacs_string(line)))
    return [puzzle_size, puzzles]

from sympy.logic.utilities.dimacs import load_file,load
from os.path import join
import math

sudoku_rules_path = "input"

sudoku_rules = {
    4 : "sudoku-rules-4x4.txt",
    9 : "sudoku-rules-9x9.txt",
   16 : "sudoku-rules-16x16.txt"
}

# For SUDOKU-16, 10-16 become A-E
def letter_gen(x):
    if x >= 10:
        return chr(ord('A') + x - 10)
    else:
        return str(x)

# Converts one line of dot format (one puzzle) into DIMACS
def get_dimacs_string(line):
    sudoku_string = ""
    cnt = 0
    sudoku_size =  math.isqrt(len(line))
    for tok in line:
        cnt += 1
        if tok.isalnum():
            sudoku_string += letter_gen((cnt - 1) // sudoku_size + 1)
            sudoku_string += letter_gen(cnt % sudoku_size if cnt % sudoku_size != 0 else sudoku_size)
            sudoku_string += tok
            sudoku_string += " 0\n"
    return sudoku_string


# Gets the SUDOKU rules corresponding to the size as CNF clause
def parse_sudoku_rules(sudoku_size):
    return load_file(join(sudoku_rules_path, sudoku_rules[sudoku_size]))

# Gets the puzzles from the file as SAT CNF clauses
def parse_sudoku_puzzles(puzzles_file):
    puzzles = []
    line = puzzles_file.readline()
    puzzles.append(load(get_dimacs_string(line)))
    puzzle_size = math.isqrt(len(line))

    for line in puzzles_file.readline():
        puzzles.append(load(get_dimacs_string(line)))

    return puzzle_size, puzzles

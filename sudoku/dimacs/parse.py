#from sympy.logic.utilities.dimacs import load_file,load
from os.path import join
import math
import re

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
    return load_dimacs_file(join(sudoku_rules_path, sudoku_rules[sudoku_size]))

# Gets the puzzles from the file as SAT CNF clauses
def parse_sudoku_puzzles(puzzles_file):
    puzzles = []
    all_predicates = set()
    line = puzzles_file.readline()
    clauses, predicates = dimacs_to_cnf(get_dimacs_string(line))
    puzzles.append(clauses)
    all_predicates = all_predicates.union(predicates)
    puzzle_size = math.isqrt(len(line))

    for line in puzzles_file.readline():
        clauses, predicates = dimacs_to_cnf(get_dimacs_string(line))
        puzzles.append(clauses)
        all_predicates = all_predicates.union(predicates)
    return puzzle_size, puzzles, all_predicates

# Converts a string in DIMACS format to a CNF as a list of sets
# Does not validate DIMACS format, assumes input is correct
def dimacs_to_cnf(dimacs_string):
    clauses = []
    predicates = set()
    rows = dimacs_string.split('\n')
    # Exclude comments or summary
    exclusion_regex = re.compile('(c.*|p\s*cnf\s*(\d*)\s*(\d*))')

    for row in rows:
        if not exclusion_regex.match(row):
            literals = row.rstrip('0').split()
            clause = set()
            for literal in literals:
                #int_literal = int(literal)
                clause.add(literal)
                predicates.add(literal.lstrip('-'))
            if len(clause) > 0:
                clauses.append(clause)
    return clauses, predicates

# Reads a DIMACS from a file into a CNF expression as a list of sets
def load_dimacs_file(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return dimacs_to_cnf(content)

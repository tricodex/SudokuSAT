from parser.parse_clauses import parse_sudoku_rules,parse_sudoku_puzzles
from sympy.logic.boolalg import Or, Not, And

# Solves all puzzles in the file with the given strategy (1,2,3)
def solve_all(strategy, puzzles_file):
    size, puzzles = parse_sudoku_puzzles(puzzles_file);
    rules = parse_sudoku_rules(size)
    for puzzle in puzzles:
        clauses = And(puzzle, rules)
        solve(strategy, clauses)

# Solves the SAT problem for the clauses in CNF and the given strategy (1,2,3)
def solve(strategy, clauses):
    return None

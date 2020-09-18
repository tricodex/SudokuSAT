#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from ..dimacs.parse import parse_sudoku_rules,parse_sudoku_puzzles
from ..dimacs.export import export_to_dimacs
import string

# Solves all puzzles in the file with the given strategy (1,2,3)
def solve_all(strategy, puzzles_file):
    size, puzzles, _ = parse_sudoku_puzzles(puzzles_file);
    rules, symbols = parse_sudoku_rules(size)
    for puzzle in puzzles:
        formula = puzzle + rules
        export_to_dimacs(solve(strategy, formula, symbols))

# Solves the SAT problem for the formula in CNF and the given strategy (1,2,3)
def solve(strategy, formula, symbols):
    formula_int, symbols_int = get_formula_int(formula, symbols)
    result = dpll(strategy, formula_int, symbols_int, {})
    return get_result_string(result)

# Converts the literals in the formula from string to int
def get_formula_int(formula, symbols):
    symbols = sorted(symbols)
    symbols_map = dict((symbols[i - 1], i) for i in range (1, len(symbols) + 1))
    symbols_int = set(symbols_map.values())

    formula_int = []
    for clause in formula:
        formula_int.append(set(get_literal_int(literal, symbols_map) for literal in clause))
    return formula_int, symbols_int

# Converts one literal from string to int
def get_literal_int(literal, symbols_map):
    if literal.startswith('-'):
        return -symbols_map[literal.lstrip('-')]
    else:
       return symbols_map[literal]

# Converts the symbols in the truth assigment map from int to original string
def get_result_string(result):
    return result

# Solves the Sudoku SAT using DPLL algorithm
def dpll(strategy, formula, symbols, model):
    symbols, formula, model = simplify(symbols, formula, model, first_unit_clause)
    symbols, formula, model = simplify(symbols, formula, model, first_pure_symbol)

    satisfied, formula = check_if_sat(formula, model)
    if satisfied is False:
        return False
    if satisfied is True:
        return model

    # Branching based on strategy 1,2 or 3
    symbol,model_pos,model_neg = get_next_symbol(strategy, symbols, formula, model)

    return (dpll(strategy, unit_propagation(formula, symbol), symbols - {symbol}, model_pos) or
            dpll(strategy, unit_propagation(formula, -symbol), symbols - {symbol}, model_neg))

# Perform given simplification of the formula iteratively until no longer possible
def simplify(symbols, formula, model, simplification_logic):
    symbol, value = simplification_logic(formula, model)
    while symbol:
        model[symbol] = value
        symbols.remove(symbol)
        formula = unit_propagation(formula, symbol if value else -symbol)
        symbol, value = simplification_logic(formula, model)
    return symbols, formula, model

# TODO: Returns the next symbol based on the branching strategy
def get_next_symbol(strategy, symbols, formula, model):
    symbol = symbols.pop()
    model_neg = model.copy()
    model[symbol] = True
    model_neg[symbol] = False
    return symbol, model, model_neg

# Checks if the formula is satisfied with the given model
# The formula is satisfied if all clauses are true
# If there is at least one clause that cannot be determined, the result is None
def check_if_sat(formula, model):
    unknown_clauses = []
    for c in formula:
        val = is_clause_true(c, model)
        if val is True:
            continue
        # Backtrack
        if val is False:
            return False, unknown_clauses
        unknown_clauses.append(c)
    if not unknown_clauses:
        return True, unknown_clauses
    return None, unknown_clauses

# Gets the symbol that forms the first remaining unit clause together
# with its truth value
def first_unit_clause(formula, model):
    for clause in formula:
        unbound_literals = clause - set(model) - set(-s for s in model)
        if len(unbound_literals) == 1:
            lit = unbound_literals.pop()
            return abs(lit), lit > 0
    return None, None

# (1) Removes unit clause with positive (true) literal
# (2) Removes negative (false) occurences of literal from all clauses
def unit_propagation(formula, lit):
    return [clause - {-lit} for clause in formula if lit not in clause]

# Gets the first occuring pure symbol, i.e occurs only as s or -s
def first_pure_symbol(formula, model):
    unbound_literals = set().union(*formula) - set(model) - set(-s for s in model)
    positive_literals = set(lit for lit in unbound_literals if lit > 0)
    negative_literals = set(lit for lit in unbound_literals if lit < 0)
    negative_literal_symbols = set(abs(lit) for lit in negative_literals)

    for p in positive_literals - negative_literal_symbols:
        return p, True
    for p in negative_literal_symbols - positive_literals:
        return -p, False
    return None, None

# Checks if a clause resolves to true, false or unknown
def is_clause_true(clause, model={}):
    result = False
    for lit in clause:
        value = model.get(abs(lit))
        if value is not None:
            value = value if lit >= 0 else not value
            if value is True:
                return True
        else:
            result = None
    return result

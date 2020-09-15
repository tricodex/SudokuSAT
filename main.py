import argparse
from solver.sat import solve_all

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-S","--strategy", type=int, choices=range(1,4), help="The strategy to use: S1, S2 or S3")
    ap.add_argument("puzzles_filename", type=argparse.FileType('r'), help="the filename containing the SUDOKU puzzles to solve")
    args = vars(ap.parse_args())

    print("Solving SUDOKU SAT with {} on {}...".format(args['strategy'],args['puzzles_filename']))

    # TODO: call the parser for the puzzle and solver with the strategy provided
    solve_all(args['strategy'],args['puzzles_filename'])

if __name__ == "__main__":
    main()

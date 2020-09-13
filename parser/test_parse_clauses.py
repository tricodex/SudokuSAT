from parse_clauses import *

import unittest
sudoku_line_4 = "...3..4114..3..."
sudoku_dimacs_4 = """143 0
234 0
241 0
311 0
324 0
413 0
"""

sudoku_line_9 = "52...6.........7.13...........4..8..6......5...........418.........3..2...87....."

sudoku_dimacs_9 = """115 0
122 0
166 0
277 0
291 0
313 0
444 0
478 0
516 0
585 0
724 0
731 0
748 0
853 0
882 0
938 0
947 0
"""
class TestStringMethods(unittest.TestCase):


    def test_get_dimacs_string(self):
        self.assertEqual(get_dimacs_string(sudoku_line_4), sudoku_dimacs_4)
        self.assertEqual(get_dimacs_string(sudoku_line_9), sudoku_dimacs_9)

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
    print("All parser tests passed")

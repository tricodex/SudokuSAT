from .sat import solve
import unittest
from tempfile import TemporaryFile

generic_clauses_1 = [{'1','-2'},{'2','3'},{'1','3','4'},{'-1'}]
generic_predicates_1 = {'1','2','3','4'}
generic_truth_sat_1 = {1:False, 2:False, 3:True}

generic_clauses_2 = [{'1','-2'},{'2','3'},{'-3'}]
generic_predicates_2 = {'1','2','3'}
generic_truth_sat_2 = {1:True, 2:True, 3:False}

generic_clauses_3 = [{'A','-B'},{'B'},{'-A'}]
generic_predicates_3 = {'A','B'}
generic_truth_sat_3 = False

class TestSolveMethod(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, generic_clauses_1, generic_predicates_1),
            generic_truth_sat_1)
        self.assertEqual(solve(1, generic_clauses_2, generic_predicates_2),
            generic_truth_sat_2)
        self.assertEqual(solve(1, generic_clauses_3, generic_predicates_3),
            generic_truth_sat_3)

if __name__ == '__main__':
    unittest.main()
    print("All solver tests passed")

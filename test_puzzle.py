import unittest
from puzzle import Puzzle


class TestPuzzle(unittest.TestCase):

    def test_solved_board_is_solved_4x4(self):
        p = Puzzle(size=4)
        self.assertTrue(p.is_solved())

    def test_solved_board_is_solved_3x3(self):
        p = Puzzle(size=3)
        self.assertTrue(p.is_solved())

    def test_move_adjacent_tile_works_4x4(self):
        p = Puzzle(size=4)
        moved = p.move(14)   # tile 15 moves into blank at index 15
        self.assertTrue(moved)
        self.assertEqual(p.board[15], 15)
        self.assertEqual(p.board[14], 0)
        self.assertEqual(p.moves, 1)

    def test_illegal_move_does_not_work_4x4(self):
        p = Puzzle(size=4)
        moved = p.move(0)
        self.assertFalse(moved)
        self.assertEqual(p.board, list(range(1, 16)) + [0])
        self.assertEqual(p.moves, 0)

    def test_move_adjacent_tile_works_3x3(self):
        p = Puzzle(size=3)
        moved = p.move(7)   # tile 8 moves into blank at index 8
        self.assertTrue(moved)
        self.assertEqual(p.board[8], 8)
        self.assertEqual(p.board[7], 0)
        self.assertEqual(p.moves, 1)

    def test_illegal_move_does_not_work_3x3(self):
        p = Puzzle(size=3)
        moved = p.move(0)
        self.assertFalse(moved)
        self.assertEqual(p.board, list(range(1, 9)) + [0])
        self.assertEqual(p.moves, 0)

    def test_scramble_changes_board_4x4(self):
        p = Puzzle(size=4)
        before = p.board[:]
        p.scramble()
        after = p.board[:]
        self.assertNotEqual(before, after)

    def test_scramble_changes_board_3x3(self):
        p = Puzzle(size=3)
        before = p.board[:]
        p.scramble()
        after = p.board[:]
        self.assertNotEqual(before, after)

    def test_move_count_resets_after_scramble(self):
        p = Puzzle(size=4)
        p.move(14)
        self.assertEqual(p.moves, 1)
        p.scramble()
        self.assertEqual(p.moves, 0)

    def test_scramble_is_solvable_4x4(self):
        p = Puzzle(size=4)
        for _ in range(10):
            p.scramble()
            self.assertTrue(p.is_solvable())

    def test_scramble_is_solvable_3x3(self):
        p = Puzzle(size=3)
        for _ in range(10):
            p.scramble()
            self.assertTrue(p.is_solvable())

    def test_valid_move_indices_solved_4x4(self):
        p = Puzzle(size=4)
        self.assertEqual(set(p.valid_move_indices()), {11, 14})

    def test_valid_move_indices_solved_3x3(self):
        p = Puzzle(size=3)
        self.assertEqual(set(p.valid_move_indices()), {5, 7})

    def test_diagonal_move_disabled_by_default(self):
        p = Puzzle(size=3, allow_diagonal=False)
        # Put blank in center and test that corner cannot move diagonally
        p.board = [
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ]
        moved = p.move(0)  # diagonal to center, should fail
        self.assertFalse(moved)

    def test_diagonal_move_enabled(self):
        p = Puzzle(size=3, allow_diagonal=True)
        p.board = [
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ]
        moved = p.move(0)  # diagonal to center, should work now
        self.assertTrue(moved)
        self.assertEqual(p.board[0], 0)
        self.assertEqual(p.board[4], 1)
        self.assertEqual(p.moves, 1)


if __name__ == "__main__":
    unittest.main()
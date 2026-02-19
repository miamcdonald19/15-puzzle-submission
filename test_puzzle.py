import unittest
from puzzle import Puzzle

class TestPuzzle(unittest.TestCase):

    def test_solved_board_is_solved(self):
        p = Puzzle()
        self.assertTrue(p.is_solved())

    def test_move_adjacent_tile_works(self):
        # In a solved board, the empty space is at index 15,
        # and the tile at index 14 is adjacent and should move.
        p = Puzzle()
        moved = p.move(14)
        self.assertTrue(moved)
        self.assertEqual(p.board[15], 15)
        self.assertEqual(p.board[14], 0)
        self.assertEqual(p.moves, 1)

    def test_illegal_move_does_not_work(self):
        # index 0 is not adjacent to empty index 15, so it should not move
        p = Puzzle()
        moved = p.move(0)
        self.assertFalse(moved)
        self.assertEqual(p.board, list(range(1, 16)) + [0])
        self.assertEqual(p.moves, 0)

    def test_scramble_changes_board(self):
        p = Puzzle()
        before = p.board[:]
        p.scramble()
        after = p.board[:]
        self.assertNotEqual(before, after)

    def test_move_count_resets_after_scramble(self):
        p = Puzzle()
        p.move(14)  # legal move
        self.assertEqual(p.moves, 1)
        p.scramble()
        self.assertEqual(p.moves, 0)

if __name__ == "__main__":
    unittest.main()

from src.core.board import Board
import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(5, 5)

    def test_initial_state(self):
        self.assertEqual(self.board.width, 5)
        self.assertEqual(self.board.height, 5)
        self.assertEqual(len(self.board.cells), 5)
        for row in self.board.cells:
            self.assertEqual(len(row), 5)

    def test_repr(self):
        self.assertEqual(repr(self.board), "Board(width=5, height=5)")

    def test_equality(self):
        another_board = Board(5, 5)
        self.assertEqual(self.board, another_board)
        another_board.cells[0][0].adjacent_mines = 1
        self.assertNotEqual(self.board, another_board)

    def test_inequality(self):
        another_board = Board(4, 4)
        self.assertNotEqual(self.board, another_board)

    def test_get_cell(self):
        cell = self.board.get_cell(2, 2)
        self.assertIsNotNone(cell)
        self.assertEqual(cell.adjacent_mines, 0)
        
        out_of_bounds_cell = self.board.get_cell(10, 10)
        self.assertIsNone(out_of_bounds_cell)


if __name__ == "__main__":
    unittest.main()
import unittest

from src.core.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board(5, 5)

    def test_initial_state(self) -> None:
        self.assertEqual(self.board.width, 5)
        self.assertEqual(self.board.height, 5)
        self.assertEqual(len(self.board.cells), 5)
        for row in self.board.cells:
            self.assertEqual(len(row), 5)

    def test_repr(self) -> None:
        self.assertEqual(repr(self.board), "Board(width=5, height=5)")

    def test_equality(self) -> None:
        another_board = Board(5, 5)
        self.assertEqual(self.board, another_board)
        another_board.cells[0][0].adjacent_mines = 1
        self.assertNotEqual(self.board, another_board)

    def test_inequality(self) -> None:
        another_board = Board(4, 4)
        self.assertNotEqual(self.board, another_board)

    def test_get_cell(self) -> None:
        cell = self.board.get_cell(2, 2)
        self.assertIsNotNone(cell)
        self.assertEqual(cell.adjacent_mines, 0)

        out_of_bounds_cell = self.board.get_cell(10, 10)
        self.assertIsNone(out_of_bounds_cell)

    def test_get_random_cell(self) -> None:
        cell = self.board.get_random_cell()
        self.assertIsNotNone(cell)
        self.assertIn(cell, [c for row in self.board.cells for c in row])
        self.assertEqual(cell.adjacent_mines, 0)

    def test_get_revealed_count(self) -> None:
        # Initially, no cells are revealed
        self.assertEqual(self.board.get_revealed_count(), 0)

        # Reveal a cell and check the count
        cell = self.board.get_cell(0, 0)
        cell.reveal()
        self.assertEqual(self.board.get_revealed_count(), 1)

        # Reveal another cell
        cell = self.board.get_cell(1, 1)
        cell.reveal()
        self.assertEqual(self.board.get_revealed_count(), 2)


if __name__ == "__main__":
    unittest.main()

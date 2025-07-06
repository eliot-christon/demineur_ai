import unittest

from src.core.cell import Cell


class TestCell(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a Cell instance for testing."""
        self.cell = Cell()

    def test_initial_state(self) -> None:
        self.assertEqual(self.cell.adjacent_mines, 0)
        self.assertFalse(self.cell.is_revealed())
        self.assertFalse(self.cell.is_mine())
        self.assertFalse(self.cell.is_flagged())

    def test_reveal(self) -> None:
        self.cell.reveal()
        self.assertTrue(self.cell.is_revealed())

    def test_toggle_flag(self) -> None:
        self.cell.toggle_flag()
        self.assertTrue(self.cell.is_flagged())
        self.cell.toggle_flag()
        self.assertFalse(self.cell.is_flagged())

    def test_set_adjacent_mines(self) -> None:
        self.cell.adjacent_mines = 3
        self.assertEqual(self.cell.adjacent_mines, 3)

        with self.assertRaises(ValueError):
            self.cell.adjacent_mines = -2

    def test_is_mine(self) -> None:
        self.assertFalse(self.cell.is_mine())
        self.cell.adjacent_mines = -1
        self.assertTrue(self.cell.is_mine())


if __name__ == "__main__":
    unittest.main()

import unittest

from src.core.board import Board
from src.core.player import HumanPlayer, RandomPlayer


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test case with a human player and a random player."""
        self.human_player = HumanPlayer("HumanPlayer")
        self.random_player = RandomPlayer("RandomPlayer")

    def test_player_initialization(self) -> None:
        self.assertEqual(
            self.human_player.name, "HumanPlayer", "Human player name should be 'HumanPlayer'."
        )
        self.assertEqual(
            self.random_player.name, "RandomPlayer", "Random player name should be 'RandomPlayer'."
        )

    def test_make_move(self) -> None:
        """Test the make_move method for both human and random players."""
        board = Board(5, 5)

        self.assertIsNone(
            self.human_player.make_move(board), "Human player should return None for make_move."
        )

        random_move = self.random_player.make_move(board)
        self.assertIsInstance(
            random_move, tuple, "Random player should return a tuple for make_move."
        )
        self.assertEqual(
            len(random_move), 3, "Random player move should be a tuple of (x, y, action)."
        )
        self.assertIn(
            random_move[2],
            ["reveal", "flag"],
            "Random player action should be either 'reveal' or 'flag'.",
        )
        self.assertTrue(
            0 <= random_move[0] < board.width,
            "Random player x coordinate should be within board width.",
        )
        self.assertTrue(
            0 <= random_move[1] < board.height,
            "Random player y coordinate should be within board height.",
        )


if __name__ == "__main__":
    unittest.main()

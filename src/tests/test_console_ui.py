import unittest

from src.core.player import RandomPlayer
from src.ui.console_ui import ConsoleUI
from src.core.game_logic import GameLogic


class TestConsoleUI(unittest.TestCase):
    def setUp(self):

        self.game_logic = GameLogic(
            width=9, height=5, mine_count=10, player=RandomPlayer(name="TestPlayer")
        )
        self.console_ui = ConsoleUI(self.game_logic)

    def test_start_game(self):
        # This test will not run as expected since it requires user input.
        # Instead, we can test the initial setup and display methods.
        self.assertIsNotNone(self.console_ui.game_logic)
        self.assertEqual(self.console_ui.game_logic.player.name, "TestPlayer")

    def test_display_board(self):
        # Test if the board is displayed correctly
        self.console_ui.display_board()
        # Normally we would capture stdout to verify the output, but here we just check if no exceptions are raised.

        # reveal all cells to test display
        for x in range(self.game_logic.board.width):
            for y in range(self.game_logic.board.height):
                self.game_logic.board.get_cell(x, y).reveal()
        self.console_ui.display_board()


if __name__ == "__main__":
    unittest.main()

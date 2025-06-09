from src.ui.console_ui import ConsoleUI
import unittest

class TestConsoleUI(unittest.TestCase):
    def setUp(self):
        from src.core.game_logic import GameLogic
        self.game_logic = GameLogic(width=5, height=5, mine_count=10, player_name="TestPlayer")
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
        for x in range(5):
            for y in range(5):
                self.game_logic.board.get_cell(x, y).reveal()
        self.console_ui.display_board()
        

if __name__ == "__main__":
    unittest.main()
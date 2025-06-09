from src.core.game_logic import GameLogic
import unittest

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game_logic_no_mines = GameLogic(width=5, height=5, mine_count=0, player_name="TestPlayer1")
        self.game_logic_only_mines = GameLogic(width=5, height=5, mine_count=25, player_name="TestPlayer2")
        
    def test_initial_state(self):
        self.assertFalse(self.game_logic_no_mines.is_game_over())
        self.assertFalse(self.game_logic_no_mines.is_game_won())
    
    def test_make_move_reveal(self):
        # Test revealing a cell
        result = self.game_logic_no_mines.make_move(0, 0, "reveal")
        self.assertTrue(result)
        self.assertFalse(self.game_logic_no_mines.is_game_over())
        
        # Test revealing a mine
        # Assuming the mine is placed at (1, 1) for this test
        self.game_logic_only_mines.make_move(1, 1, "reveal")
        self.assertFalse(self.game_logic_only_mines.is_game_won())
        self.assertTrue(self.game_logic_only_mines.is_game_over())
    
    def test_make_move_flag(self):
        # Test flagging a cell
        result = self.game_logic_no_mines.make_move(0, 0, "flag")
        self.assertTrue(result)
        self.assertFalse(self.game_logic_no_mines.is_game_over())
    
    def test_make_move_invalid_action(self):
        # Test invalid action
        result = self.game_logic_no_mines.make_move(0, 0, "invalid_action")
        self.assertFalse(result)
        self.assertFalse(self.game_logic_no_mines.is_game_over())
        

if __name__ == "__main__":
    unittest.main()
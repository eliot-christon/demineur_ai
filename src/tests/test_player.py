from src.core.player import Player, HumanPlayer, RandomPlayer
from src.core.board import Board
import unittest


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.human_player = HumanPlayer("HumanPlayer")
        self.random_player = RandomPlayer("RandomPlayer")
    
    def test_player_initialization(self):
        self.assertEqual(self.human_player.name, "HumanPlayer", "Human player name should be 'HumanPlayer'.")
        self.assertEqual(self.random_player.name, "RandomPlayer", "Random player name should be 'RandomPlayer'.")
    
    def test_make_move(self):
        board = Board(5, 5)
        
        human_move = self.human_player.make_move(board)
        self.assertIsNone(human_move, "Human player should return None for make_move.")
        
        random_move = self.random_player.make_move(board)
        self.assertIsInstance(random_move, tuple, "Random player should return a tuple for make_move.")
        self.assertEqual(len(random_move), 3, "Random player move should be a tuple of (x, y, action).")
        self.assertIn(random_move[2], ["reveal", "flag"], "Random player action should be either 'reveal' or 'flag'.")
        self.assertTrue(0 <= random_move[0] < board.width, "Random player x coordinate should be within board width.")
        self.assertTrue(0 <= random_move[1] < board.height, "Random player y coordinate should be within board height.")
        

if __name__ == "__main__":
    unittest.main()
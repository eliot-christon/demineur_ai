from src.core.player import HumanPlayer, RandomPlayer
from src.core.game_logic import GameLogic
from src.ui.graphical_ui import GraphicalUI
    

def main():
    """Main function to start the game."""
    # Initialize the game logic with a human player
    game_logic = GameLogic(width=10, height=10, mine_count=20, player=HumanPlayer(name="Player1"))
    
    # Create the graphical UI for the game
    graphical_ui = GraphicalUI(game_logic)
    
    # Start the game
    graphical_ui.start_game()


if __name__ == "__main__":
    main()
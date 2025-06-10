from src.core.player import HumanPlayer, RandomPlayer, ProbaPlayer
from src.core.game_logic import GameLogic
from src.ui.graphical_ui import GraphicalUI
from src.ui.console_ui import ConsoleUI
    

def main():
    """Main function to start the game."""
    # Initialize the game logic with a human player
    game_logic = GameLogic(width=10, height=10, mine_count=10, player=ProbaPlayer(name="Player1"))
    
    # Create the UI for the game
    ui = GraphicalUI(game_logic)
    
    # Start the game
    ui.start_game()


if __name__ == "__main__":
    main()
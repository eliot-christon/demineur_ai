from src.core.game_logic import GameLogic
from src.core.player import ProbaPlayer
from src.ui.graphical_ui import GraphicalUI


def main() -> int:
    """Main function to start the game."""
    # Initialize the game logic with a human player
    game_logic = GameLogic(width=12, height=8, mine_count=18, player=ProbaPlayer(name="Player1"))

    # Create the UI for the game
    ui = GraphicalUI(game_logic)

    # Start the game
    ui.start_game()

    return 0


if __name__ == "__main__":
    main()

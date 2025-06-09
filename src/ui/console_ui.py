from src.core.game_logic import GameLogic

class ConsoleUI:
    def __init__(self, game_logic: GameLogic) -> None:
        """Initialize the console UI with the game logic."""
        self.game_logic = game_logic

    def start_game(self) -> None:
        """Start the game and handle user input."""
        print(f"Welcome to Minesweeper, {self.game_logic.player.name}!")
        while not self.game_logic.is_game_over():
            self.display_board()
            action = input("Enter your move (x y action): ").strip().split()
            if len(action) != 3:
                print("Invalid input. Please enter in the format: x y action")
                continue
            
            try:
                x, y = int(action[0]), int(action[1])
                action_type = action[2].lower()
                if not self.game_logic.make_move(x, y, action_type):
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid coordinates. Please enter integers for x and y.")

        self.display_result()

    def display_board(self) -> None:
        """Display the current state of the board."""
        board = self.game_logic.board
        print("\nCurrent Board:\n" + "-" * (board.width * 2 + 3))
        for row in board.cells:
            print("| ", end="")
            for cell in row:
                if cell.is_revealed():
                    if cell.is_mine():
                        print("M", end=" ")
                    else:
                        print(cell.adjacent_mines, end=" ")
                elif cell.is_flagged():
                    print("F", end=" ")
                else:
                    print("?", end=" ")
            print("|")
        print("-" * (board.width * 2 + 3))

    def display_result(self) -> None:
        """Display the result of the game."""
        if self.game_logic.is_game_won():
            print(f"Congratulations {self.game_logic.player.name}, you won!")
        else:
            print(f"Game over! Better luck next time, {self.game_logic.player.name}.")


# Example usage:
if __name__ == "__main__":
    game_logic = GameLogic(width=5, height=5, mine_count=5, player_name="Player1")
    console_ui = ConsoleUI(game_logic)
    console_ui.start_game()
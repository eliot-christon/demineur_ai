from src.core.game_logic import GameLogic
from src.ui.colors import bg, fg


class ConsoleUI:
    def __init__(self, in_game_logic: GameLogic) -> None:
        """Initialize the console UI with the game logic."""
        self.game_logic = in_game_logic
        self.__color_per_char = {
            "0": fg.green,
            "1": fg.lightgreen,
            "2": fg.blue,
            "3": fg.lightblue,
            "4": fg.yellow,
            "5": fg.orange,
            "6": fg.purple,
            "7": fg.pink,
            "8": fg.lightgrey,
        }

    def start_game(self) -> None:
        """Start the game and handle user input."""
        print(f"Welcome to Minesweeper, {self.game_logic.player.name}!")
        while not self.game_logic.is_game_over():
            self.display_board()
            action = self.game_logic.player.make_move(self.game_logic.board)
            if action is None:
                action_input = input("Enter your move (x y action): ").strip().split()
                action = [int(coord) for coord in action_input[:2]] + action_input[2]
            if len(action) == 2:
                action.append("reveal")
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

        self.display_board()
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
                        print(bg.red + "M" + bg.res, end=" ")
                    else:
                        print(
                            self.__color_per_char.get(str(cell.adjacent_mines), "")
                            + str(cell.adjacent_mines)
                            + fg.res,
                            end=" ",
                        )
                elif cell.is_flagged():
                    print(bg.orange + fg.bold + "F" + bg.res + fg.res, end=" ")
                else:
                    print(bg.blue + "?" + bg.res, end=" ")
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
    from src.core.player import HumanPlayer

    game_logic = GameLogic(width=5, height=5, mine_count=5, player=HumanPlayer(name="Player1"))
    console_ui = ConsoleUI(game_logic)
    console_ui.start_game()

from src.core.board import Board
from src.core.player import Player


class GameLogic:
    def __init__(self, width: int, height: int, mine_count: int, player_name: str) -> None:
        """Initialize the game logic with a board of given dimensions and mine count."""
        self.__board = Board(width, height)
        self.__mine_count = mine_count
        self.__place_mines()
        self.__player = Player(player_name)
        self.__game_over = False
        self.__game_won = False
        
    def __place_mines(self) -> None:
        """Randomly place mines on the board."""
        count = 0
        while count < self.__mine_count:
            cell = self.__board.get_random_cell()
            if not cell.is_mine():
                cell.adjacent_mines = -1
                count += 1
    
    def make_move(self, x: int, y: int, action: str= "reveal") -> bool:
        """Make a move with the specified action at coordinates (x, y)."""
        if self.__game_over:
            return False
        
        cell = self.__board.get_cell(x, y)
        
        if action == "reveal":
            if cell.is_mine():
                self.__game_over = True
                self.__game_won = False
                self.__player.notify(f"{self.__player.name} hit a mine at ({x}, {y}). Game Over!")
            else:
                cell.reveal()
                self.__player.notify(f"{self.__player.name} revealed cell at ({x}, {y}).")
                if self.__check_win_condition():
                    self.__game_over = True
                    self.__game_won = True
                    self.__player.notify(f"{self.__player.name} has won the game!")
        elif action == "flag":
            if not cell.is_revealed():
                cell.toggle_flag()
                self.__player.notify(f"{self.__player.name} toggled flag at ({x}, {y}).")
            else:
                self.__player.notify(f"{self.__player.name} cannot flag a revealed cell at ({x}, {y}).")
                return False
        else:
            self.__player.notify(f"{self.__player.name} made an invalid move: ({x}, {y}) with action: {action}.")
            return False
        
        return True
                
    def __check_win_condition(self) -> bool:
        """Check if the player has won the game."""
        for row in self.__board.cells:
            for cell in row:
                if not cell.is_mine() and not cell.is_revealed():
                    return False
        return True
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.__game_over
    
    def is_game_won(self) -> bool:
        """Check if the game has been won."""
        return self.__game_won
    
    def get_board(self) -> Board:
        """Get the current state of the board."""
        return self.__board
    
from src.core.board import Board
from src.core.player import Player


class GameLogic:
    def __init__(self, width: int, height: int, mine_count: int, player: Player) -> None:
        """Initialize the game logic with a board of given dimensions and mine count."""
        self.__board = Board(width, height)
        self.__mine_count = mine_count
        self.__place_mines()
        self.__init_adjacent_mine_counts()
        self.__player = player
        self.__game_over = False
        self.__game_won = False
        
    def __place_mines(self) -> None:
        """Randomly place mines on the board."""
        count = 0
        if self.__mine_count > self.__board.width * self.__board.height:
            raise ValueError("Mine count exceeds the number of cells on the board.")
        while count < self.__mine_count:
            cell = self.__board.get_random_cell()
            if not cell.is_mine():
                cell.adjacent_mines = -1
                count += 1
    
    def __init_adjacent_mine_counts(self) -> None:
        """Initialize the adjacent mine counts for each cell."""
        for y in range(self.__board.height):
            for x in range(self.__board.width):
                cell = self.__board.get_cell(x, y)
                if not cell.is_mine():
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            neighbor = self.__board.get_cell(x + dx, y + dy)
                            if neighbor and neighbor.is_mine():
                                count += 1
                    cell.adjacent_mines = count
    
    def make_move(self, x: int, y: int, action: str= "reveal") -> bool:
        """Make a move with the specified action at coordinates (x, y)."""
        if self.__game_over:
            return False
        
        cell = self.__board.get_cell(x, y)
        
        if cell is None:
            return False
        
        if action == "reveal":
            cell.reveal()
            if cell.is_mine():
                self.__game_over = True
                self.__game_won = False
            else:
                if self.__check_win_condition():
                    self.__game_over = True
                    self.__game_won = True
        elif action == "flag":
            if not cell.is_revealed():
                cell.toggle_flag()
            else:
                return False
        else:
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
    
    @property
    def board(self) -> Board:
        """Get the current state of the board."""
        return self.__board

    @property
    def player(self) -> Player:
        """Get the current player."""
        return self.__player
    
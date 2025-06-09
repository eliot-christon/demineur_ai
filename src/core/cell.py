

class Cell:
    def __init__(self, adjacent_mines:int=0) -> None:
        self.__revealed = False
        self.__flagged = False
        self.__adjacent_mines = adjacent_mines

    def __repr__(self) -> str:
        return f"Cell(adjacent_mines={self.__adjacent_mines})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Cell):  return False
        if self.__adjacent_mines != other.adjacent_mines:  return False
        return True
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    @property
    def adjacent_mines(self) -> int:
        return self.__adjacent_mines
    
    @adjacent_mines.setter
    def adjacent_mines(self, count:int) -> None:
        if not isinstance(count, int) or count not in [-1] + list(range(9)):
            raise ValueError("adjacent_mines must be an integer between 0 and 8.")
        self.__adjacent_mines = count
    
    def is_mine(self) -> bool:
        return self.__adjacent_mines == -1
    
    def is_flagged(self) -> bool:
        return self.__flagged
    
    def is_revealed(self) -> bool:
        return self.__revealed
    
    def reveal(self) -> None:
        self.__revealed = True
    
    def toggle_flag(self) -> None:
        self.__flagged = not self.__flagged
        
        

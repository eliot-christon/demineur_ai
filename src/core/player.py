from src.core.board import Board

from typing import Tuple, Optional
from abc import ABC, abstractmethod
from random import randint

class Player(ABC):
    """Abstract base class for a player in the game."""
    def __init__(self, name: str) -> None:
        """Initialize the player with a name."""
        self.__name = name

    def __repr__(self) -> str:
        return f"Player(name={self.__name})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):   return False
        if self.__name != other.name:       return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        """Make a move with the specified action at coordinates (x, y).
        returns a tuple containing the x, y coordinates and the action as a string.
        For the user interface to take input from human player we return None."""
        pass


class HumanPlayer(Player):
    
    def __init__(self, name: str) -> None:
        """Initialize the human player with a name."""
        super().__init__(name)
        
    """Concrete class for a human player."""
    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        return None

class RandomPlayer(Player):
    
    def __init__(self, name: str) -> None:
        """Initialize the random player with a name."""
        super().__init__(name)
        
    """Concrete class for a random player."""
    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        """Make a random move on the board."""
        x = randint(0, board.width - 1)
        y = randint(0, board.height - 1)
        action = "reveal"
        return x, y, action
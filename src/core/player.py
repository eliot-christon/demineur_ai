from src.core.observer import Observer

from typing import List

class Player:
    def __init__(self, name: str) -> None:
        """Initialize the player with a name."""
        self.__name = name
        self._observers = list[Observer]()

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

    def attach(self, observer: Observer) -> None:
        """Attach an observer to the player."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the player."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        """Notify all observers with a message."""
        for observer in self._observers:
            observer.update(message)

    def make_move(self, x: int, y: int, action: str) -> None:
        """Make a move with the specified action at coordinates (x, y)."""
        #TODO: Implement actual move logic
        self.notify(f"{self.__name} made move: ({x}, {y}) with action: {action}")
    
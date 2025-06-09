from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Abstract base class for observers that can be notified of changes.
    """

    @abstractmethod
    def update(self, message: str) -> None:
        """
        Update method to be called when the observed object changes.
        
        :param message: A message describing the change.
        """
        pass
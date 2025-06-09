from src.core.player import Player
from src.core.observer import Observer
import unittest


class MockObserver(Observer):
    def __init__(self):
        super().__init__()
        self.notifications = []

    def update(self, message: str) -> None:
        self.notifications.append(message)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")
        self.observer = MockObserver()
    
    def test_attach_observer(self):
        self.player.attach(self.observer)
        self.assertIn(self.observer, self.player._observers)
    
    def test_detach_observer(self):
        self.player.attach(self.observer)
        self.player.detach(self.observer)
        self.assertNotIn(self.observer, self.player._observers)
    
    def test_notify_observers(self):
        self.player.attach(self.observer)
        message = "Player made a move"
        self.player.notify(message)
        self.assertIn(message, self.observer.notifications)
    
    def test_make_move(self):
        self.player.attach(self.observer)
        x, y, action = 1, 2, "reveal"
        self.player.make_move(x, y, action)
        expected_message = f"TestPlayer made move: ({x}, {y}) with action: {action}"
        self.assertIn(expected_message, self.observer.notifications)
        

if __name__ == "__main__":
    unittest.main()
from src.core.observer import Observer
import unittest


class ConcreteObserver(Observer):
    def __init__(self):
        super().__init__()
        self.notifications = []

    def update(self, message: str) -> None:
        self.notifications.append(message)

class TestObserver(unittest.TestCase):
    def setUp(self):
        self.observer = ConcreteObserver()

    def test_update(self):
        message = "Test message"
        self.observer.update(message)
        self.assertIn(message, self.observer.notifications)

    def test_multiple_updates(self):
        messages = ["First message", "Second message", "Third message"]
        for msg in messages:
            self.observer.update(msg)
        self.assertEqual(self.observer.notifications, messages)

    def test_no_updates(self):
        self.assertEqual(self.observer.notifications, [])


if __name__ == "__main__":
    unittest.main()
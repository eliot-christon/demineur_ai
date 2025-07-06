from abc import ABC, abstractmethod
from random import randint
from typing import Optional, Tuple

from src.core.board import Board


class Player(ABC):
    """Abstract base class for a player in the game."""

    def __init__(self, name: str) -> None:
        """Initialize the player with a name."""
        self.__name = name

    def __repr__(self) -> str:
        return f"Player(name={self.__name})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        if self.__name != other.name:
            return False
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


class HumanPlayer(Player):
    """Concrete class for a human player."""

    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        return None


class RandomPlayer(Player):
    """Concrete class for a random player."""

    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        """Make a random move on the board."""
        x = randint(0, board.width - 1)
        y = randint(0, board.height - 1)
        action = "reveal"
        while board.get_cell(x, y).is_revealed():
            x = randint(0, board.width - 1)
            y = randint(0, board.height - 1)
        return x, y, action


class ProbaPlayer(Player):
    """
    A player that makes decisions based on probabilities.
    It will choose a random cell to reveal or flag based on the current state of the board.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__memory = None

    def make_move(self, board: Board) -> Optional[Tuple[int, str]]:
        """
        Make a move based on the current state of the board. keep track of the probabilities of each cell being a mine.
        """
        if self.__memory:
            obv_candidate = self.get_obvious_candidate()
            if obv_candidate:
                self.__memory[obv_candidate[1]][obv_candidate[0]] = -2  # Mark as revealed
                return obv_candidate

        # build a probability table of the size of the board, fill with -2 when revealed and -3 when flagged
        prob_table = [[-1 for _ in range(board.width)] for _ in range(board.height)]

        # ATTENTION: optimizing is a key to the performance of this function, as it is called every turn.

        # Precompute directions for neighbor checks
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for y in range(board.height):
            for x in range(board.width):
                cell = board.get_cell(x, y)
                if cell.is_revealed():
                    prob_table[y][x] = -2
                    # add to the neighboring cells the probability of being a mine
                    # count first the unrevealed neighbors
                    unrevealed_neighbors = 0
                    flagged_neighbors = 0
                    for dy, dx in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < board.width and 0 <= ny < board.height:
                            neighbor_cell = board.get_cell(nx, ny)
                            if neighbor_cell.is_flagged():
                                flagged_neighbors += 1
                            elif not neighbor_cell.is_revealed():
                                unrevealed_neighbors += 1
                                # put the probability of being a mine to 0.
                                prob_table[ny][nx] = max(prob_table[ny][nx], 0)

                    if unrevealed_neighbors > 0:
                        # distribute the probability of being a mine to the neighbors
                        for dy, dx in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < board.width and 0 <= ny < board.height:
                                neighbor_cell = board.get_cell(nx, ny)
                                if (
                                    not neighbor_cell.is_revealed()
                                    and not neighbor_cell.is_flagged()
                                ):
                                    potential_new_prob = (
                                        cell.adjacent_mines - flagged_neighbors + 0.01
                                    ) / unrevealed_neighbors
                                    if prob_table[ny][nx] <= 0:
                                        prob_table[ny][nx] = potential_new_prob
                                    # priroritize extrem values, under 0.1 or above 1, for either prob_table or potential_new_prob, else, take the minimum
                                    elif prob_table[ny][nx] > 1.0 or potential_new_prob > 1.0:
                                        prob_table[ny][nx] = max(
                                            prob_table[ny][nx], potential_new_prob
                                        )
                                    else:
                                        prob_table[ny][nx] = min(
                                            prob_table[ny][nx], potential_new_prob
                                        )
                elif cell.is_flagged():
                    prob_table[y][x] = -3

        self.__memory = prob_table

        # find the coordinates of the cell with the lowest probability of being a mine
        obv_candidate = self.get_obvious_candidate()
        if obv_candidate:
            self.__memory[obv_candidate[1]][obv_candidate[0]] = -2  # Mark as revealed
            return obv_candidate

        # reveal the safest not mine candidate, random if multiple
        prob_candidates = [prob for row in prob_table for prob in row if prob >= 0]
        if prob_candidates:
            lowest_prob = min(prob for row in prob_table for prob in row if prob >= 0)
            not_mine_candidates = [
                (x, y)
                for y in range(board.height)
                for x in range(board.width)
                if prob_table[y][x] == lowest_prob
            ]
            x, y = not_mine_candidates[randint(0, len(not_mine_candidates) - 1)]
            self.__memory[y][x] = -2  # Mark as revealed
            return x, y, "reveal"

        # if no candidates, return a random cell
        # If no candidates, return a random cell
        while True:
            x = randint(0, board.width - 1)
            y = randint(0, board.height - 1)
            if not (board.get_cell(x, y).is_revealed() or board.get_cell(x, y).is_flagged()):
                self.__memory[y][x] = -2  # Mark as revealed
                return x, y, "reveal"

    def display_prob_table(self, prob_table: list) -> None:
        """Display the probability table."""
        # if positive number don't forget to add a space before it for it to be aligned
        for row in prob_table:
            print(" ".join("+" * (prob >= 0) + f"{prob:.2f}" for prob in row))
        print()

    def get_obvious_candidate(self) -> Optional[Tuple[int, int, str]]:
        if not self.__memory:
            return None

        for x, row in enumerate(self.__memory):
            for y, value in enumerate(row):
                if value >= 1.0:
                    return y, x, "flag"
                if 0 < value < 0.1:
                    return y, x, "reveal"

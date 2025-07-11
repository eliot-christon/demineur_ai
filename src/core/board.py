from random import randint
from typing import List

from src.core.cell import Cell


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__cells: List[List[Cell]] = [[Cell() for _ in range(width)] for _ in range(height)]

    def __repr__(self) -> str:
        return f"Board(width={self.__width}, height={self.__height})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        if self.__width != other.width:
            return False
        if self.__height != other.height:
            return False
        if self.__cells != other.cells:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def cells(self) -> List[List[Cell]]:
        return self.__cells

    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__cells[y][x]
        raise ValueError(
            f"Invalid coordinates ({x}, {y}) for the board of size {self.__width}x{self.__height}."
        )

    def get_random_cell(self) -> Cell:
        x = randint(0, self.__width - 1)
        y = randint(0, self.__height - 1)
        return self.get_cell(x, y)

    def get_revealed_count(self) -> int:
        """Count the number of revealed cells."""
        return sum(cell.is_revealed() for row in self.__cells for cell in row)

    def get_flagged_count(self) -> int:
        """Count the number of flagged cells."""
        return sum(cell.is_flagged() for row in self.__cells for cell in row)

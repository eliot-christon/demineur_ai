from src.core.cell import Cell
from typing import List, Optional


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__cells: List[List[Cell]] = [[Cell() for _ in range(width)] for _ in range(height)]

    def __repr__(self) -> str:
        return f"Board(width={self.__width}, height={self.__height})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):    return False
        if self.__width != other.width:     return False
        if self.__height != other.height:   return False
        if self.__cells != other.cells:     return False
        return True

    def __ne__(self, other) -> bool:
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

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__cells[y][x]
        return None
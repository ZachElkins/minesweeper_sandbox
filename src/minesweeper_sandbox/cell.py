from enum import Enum
from dataclasses import dataclass
from typing import Dict

@dataclass
class Position:
    x: int
    y: int

class CellValue(Enum):
    BOMB = "B"
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

class Cell:
    state_by_num: Dict[CellValue, int] = {state.value: state for state in CellValue}

    def __init__(self):
        self.flagged: bool = False
        self.value: CellValue = None
        self.revealed = False
        self.adjacent = []
        self.pos: Position

    def set_position(self, pos: Position) -> None:
        self.pos = pos

    def set_adjacent(self, adj: list) -> None:
        self.adjacent = adj
        self.value = Cell.state_by_num[
            sum(adj_cell.value == CellValue.BOMB for adj_cell in self.adjacent)
        ]

    def reveal(self) -> bool:
        if not self.flagged:
            self.revealed = True
            return self.value == CellValue.BOMB
        return False

    def flag(self) -> int:
        if not self.revealed:
            self.flagged = not self.flagged
            return 1 if self.flagged else -1
        return 0

    def set_bomb(self) -> None:
        self.value = CellValue.BOMB

    def is_bomb(self) -> bool:
        return self.value == CellValue.BOMB

    def get_value(self) -> CellValue:
        return self.value

    def adj_cells(self) -> list:
        return self.adjacent
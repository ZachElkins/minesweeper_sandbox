import pytest
from minesweeper_sandbox.cell import Position, CellValue, Cell


def test_position_init():
    x, y = 0, 0
    pos = Position(x, y)
    assert isinstance(pos, Position)
    assert pos.x == x
    assert pos.y == y


@pytest.mark.parametrize(
    "cell_value",
    [(cell_value.value) for cell_value in CellValue]
)
def test_cell_value_init(cell_value):
    assert cell_value in [None, "B"] + list(range(9))


def test_cell_init():
    cell = Cell()
    assert isinstance(cell, Cell)
    assert not cell.flagged
    assert cell.value == CellValue.NONE
    assert not cell.revealed
    assert cell.adjacent == []
    assert cell.pos is None


def test_cell_set_position():
    cell = Cell()
    pos = Position(0, 0)
    cell.set_position(
        pos=pos
    )
    assert cell.pos == pos


def test_cell_set_adjacent():
    main_cell = Cell()
    adj_cell_1 = Cell()
    adj_cell_2 = Cell()
    adj_cell_3 = Cell()
    main_cell.set_adjacent([adj_cell_1, adj_cell_2, adj_cell_3])
    assert isinstance(main_cell.adjacent, list)
    assert main_cell.adjacent == [adj_cell_1, adj_cell_2, adj_cell_3]


def test_cell_reveal():
    cell = Cell()
    assert not cell.reveal()
    assert cell.revealed


def test_cell_reveal_bomb():
    cell = Cell()
    cell.value = CellValue.BOMB
    assert cell.reveal()


def test_cell_reveal_flagged():
    cell = Cell()
    cell.flag()
    assert not cell.reveal()
    assert not cell.revealed


def test_cell_flag_revealed():
    cell = Cell()
    cell.reveal()
    assert cell.flag() == 0


def test_cell_add_flag():
    cell = Cell()
    assert cell.flag() == 1
    assert cell.flagged


def test_cell_remove_flag():
    cell = Cell()
    cell.flag()
    assert cell.flag() == -1
    assert not cell.flagged


def test_cell_set_bomb():
    cell = Cell()
    cell.set_bomb()
    assert cell.value == CellValue.BOMB


def test_cell_is_bomb():
    cell = Cell()
    assert not cell.is_bomb()
    cell.set_bomb()
    assert cell.is_bomb()


def test_cell_get_value_bomb():
    cell = Cell()
    cell.set_bomb()


def test_cell_get_value_num():
    cell = Cell()
    cell.set_bomb()


def test_cell_get_value():
    main_cell = Cell()
    adj_cell_1 = Cell()
    adj_cell_1.value = CellValue.BOMB
    adj_cell_2 = Cell()
    adj_cell_2.value = CellValue.ZERO
    adj_cell_3 = Cell()
    adj_cell_3.value = CellValue.ZERO
    main_cell.set_adjacent([adj_cell_1, adj_cell_2, adj_cell_3])
    assert isinstance(main_cell.value, CellValue)
    assert main_cell.get_value() == CellValue.ONE
    assert isinstance(main_cell.value.value, int)
    assert main_cell.get_value().value == 1


def test_cell_get_adj_cells():
    main_cell = Cell()
    adj_cell_1 = Cell()
    adj_cell_2 = Cell()
    adj_cell_3 = Cell()
    main_cell.set_adjacent([adj_cell_1, adj_cell_2, adj_cell_3])
    assert main_cell.adj_cells() == [adj_cell_1, adj_cell_2, adj_cell_3]

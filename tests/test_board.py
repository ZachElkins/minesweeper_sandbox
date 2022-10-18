import pytest
from minesweeper_sandbox.board import Board
from minesweeper_sandbox.cell import Cell, CellValue, Position


@pytest.fixture
def board_2x1() -> Board:
    width, height, bombs = 2, 1, 1
    board = Board(width, height, bombs)
    move = Position(0, 0)
    board.populate_board(move=move)
    return board


def test_board_init():
    width, height, bombs = 2, 2, 1
    board = Board(width, height, bombs)
    assert isinstance(board, Board)
    assert board.w == width
    assert board.h == height
    assert board.bombs == bombs
    assert board.flagged_cells == 0
    assert board.revealed_cells == 0
    assert isinstance(board.board, list)


def tests_board_create_empty_board():
    width, height, bombs = 2, 2, 1
    board = Board(width, height, bombs)
    flat_board = sum(board.board, [])
    assert all(
        [isinstance(cell, Cell) for cell in flat_board]
    )
    assert len(board.board) == 2
    assert len(board.board[0]) == 2


def test_board_populate_board():
    width, height, bombs = 2, 1, 1
    board = Board(width, height, bombs)
    move = Position(0, 0)
    board.populate_board(move=move)
    assert board.board[0][0].value == CellValue.ONE
    assert board.board[0][1].value == CellValue.BOMB


def test_board_reveal_empty(board_2x1: Board):
    reveal_pos = Position(0, 0)
    assert not board_2x1.reveal(pos=reveal_pos)
    assert board_2x1.revealed_cells == 1


def test_board_reveal_bomb(board_2x1: Board):
    reveal_pos = Position(0, 1)
    assert board_2x1.reveal(pos=reveal_pos)
    assert board_2x1.revealed_cells == 1


def test_board_reveal_revealed(board_2x1):
    reveal_pos = Position(0, 1)
    board_2x1.reveal(pos=reveal_pos)
    assert not board_2x1.reveal(pos=reveal_pos)
    assert board_2x1.revealed_cells == 1


def test_board_reveal_flagged(board_2x1: Board):
    """Make sure that flagged cells do not get revealed"""
    reveal_pos = Position(0, 1)
    flag_pos = Position(0, 1)
    board_2x1.flag(pos=flag_pos)
    assert not board_2x1.reveal(pos=reveal_pos)
    # assert board_2x1.revealed_cells == 0


def test_board_flag(board_2x1: Board):
    flag_pos = Position(0, 1)
    assert board_2x1.flagged_cells == 0
    board_2x1.flag(pos=flag_pos)
    assert board_2x1.flagged_cells == 1


def tests_board_get_adj_coords():
    adj_to_top_lft = [
        pos for pos in Board.get_adj_coords(3, 3, Position(0, 0))
    ]
    adj_to_bot_rgt = [
        pos for pos in Board.get_adj_coords(3, 3, Position(2, 2))
    ]
    adj_to_center = [
        pos for pos in Board.get_adj_coords(3, 3, Position(1, 1))
    ]
    expected_adj_for_top_lft = [Position(0, 1), Position(1, 0), Position(1, 1)]
    expected_adj_for_bot_rgt = [Position(1, 1), Position(1, 2), Position(2, 1)]
    expected_adj_for_center = [
        Position(0, 0), Position(0, 1),
        Position(0, 2), Position(1, 0),
        Position(1, 2), Position(2, 0),
        Position(2, 1), Position(2, 2)
    ]
    assert adj_to_top_lft == expected_adj_for_top_lft
    assert adj_to_bot_rgt == expected_adj_for_bot_rgt
    assert adj_to_center == expected_adj_for_center

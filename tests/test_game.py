from copy import deepcopy
from enum import Enum
import pytest
from minesweeper_sandbox.game import Game, GameAction, GameDifficulty, GameDifficultyPreset, GameState
from minesweeper_sandbox.board import Board
from minesweeper_sandbox.cell import Cell, CellValue, Position


@pytest.fixture
def simple_game() -> Game:
    diff = GameDifficulty.BEGINNER
    return Game(difficulty=diff)


@pytest.fixture
def game_2x1() -> Game:
    mock_game_data = Enum('MockGameDifficulty', [("TEST", GameDifficultyPreset(width=2, height=1, bombs=1))])
    return Game(difficulty=mock_game_data.TEST)


@pytest.fixture
def state_data_2x1() -> dict:
    mock_state_data = {
        "state": GameState.PLAYING.value,
        "board": [["_", "_"]],
        "width": 2,
        "height": 1,
        "num_flagged": 0,
        "num_revealed": 0,
        "total_bombs": 1,
        "first_move": True
    }
    return mock_state_data


@pytest.fixture
def win_board_2x1() -> Board:
    MockBoard = Board(w=2, h=1, bombs=1)
    cell_00 = Cell()
    cell_00.value = CellValue.ONE
    cell_00.revealed = True
    cell_01 = Cell()
    cell_01.value = CellValue.BOMB
    cell_01.flagged = True
    MockBoard.revealed_cells = 1
    MockBoard.flagged_cells = 1
    MockBoard.board[0] = [cell_00, cell_01]
    return MockBoard


def test_game_game_difficulty_preset_init():
    width, height, bombs = 2, 2, 1
    gdp = GameDifficultyPreset(width, height, bombs)
    assert gdp.width == width
    assert gdp.height == height
    assert gdp.bombs == bombs


@pytest.mark.parametrize(
    "difficulty, values",
    [
        ("BEGINNER", (9, 9, 10)),
        ("INTERMEDIATE", (16, 16, 40)),
        ("EXPERT", (16, 30, 99))
    ]
)
def test_game_game_difficulty(difficulty, values):
    diff = GameDifficulty[difficulty]
    assert diff.value.width == values[0]
    assert diff.value.height == values[1]
    assert diff.value.bombs == values[2]


@pytest.mark.parametrize(
    "action, value",
    [
        ("REVEAL", "reveal"),
        ("FLAG", "flag"),
    ]
)
def test_game_game_action(action, value):
    action = GameAction[action]
    assert action.value == value


@pytest.mark.parametrize(
    "state, value",
    [
        ("PLAYING", "playing"),
        ("WIN", "win"),
        ("LOOSE", "loose"),
    ]
)
def test_game_game_state(state, value):
    state = GameState[state]
    assert state.value == value


def test_game_init():
    diff = GameDifficulty.BEGINNER
    game = Game(difficulty=diff)
    assert isinstance(game, Game)
    assert isinstance(game.board, Board)
    assert game.first_move
    assert game.state == GameState.PLAYING


def test_game_action_reveal(simple_game: Game):
    action = GameAction.REVEAL
    res = simple_game.action(action=action, x=0, y=0)
    assert res == GameState.PLAYING
    assert not simple_game.first_move


def test_game_action_flag(simple_game: Game):
    action = GameAction.FLAG
    res = simple_game.action(action=action, x=0, y=0)
    assert res == GameState.PLAYING
    assert simple_game.first_move


def test_game_reveal_first_move(game_2x1: Game):
    pos = Position(x=0, y=0)
    # This might be a reason to copy, rather than modify the board
    # in the actual implementation
    board_before = deepcopy(game_2x1.board.board)
    board_before_flat = sum(board_before, [])
    game_2x1.reveal(first_move=True, pos=pos)
    board_after = deepcopy(game_2x1.board.board)
    board_after_flat = sum(board_after, [])
    assert all(
        [cell.value == CellValue.NONE for cell in board_before_flat]
    )
    assert all(
        [cell.value != CellValue.NONE for cell in board_after_flat]
    )


def test_game_reveal_loose(game_2x1: Game):
    pos1 = Position(x=0, y=1)
    pos2 = Position(x=0, y=0)
    game_2x1.reveal(first_move=True, pos=pos1)
    game_2x1.reveal(first_move=False, pos=pos2)
    assert game_2x1.state == GameState.LOOSE


def test_game_reveal_win(game_2x1: Game):
    f_pos = Position(x=0, y=1)
    r_pos = Position(x=0, y=0)
    game_2x1.flag(pos=f_pos)
    game_2x1.reveal(first_move=True, pos=r_pos)
    assert game_2x1.state == GameState.WIN


def test_game_flag_first_move(game_2x1: Game):
    pos = Position(x=0, y=0)
    game_2x1.flag(pos=pos)
    board_flat = sum(game_2x1.board.board, [])
    assert all(
        [cell.value == CellValue.NONE for cell in board_flat]
    )
    assert game_2x1.board.board[0][0].flagged


def test_game_flag_win(game_2x1: Game):
    r_pos = Position(x=0, y=0)
    f_pos = Position(x=0, y=1)
    game_2x1.reveal(first_move=True, pos=r_pos)
    game_2x1.flag(pos=f_pos)
    assert game_2x1.board.board[0][1].flagged
    assert game_2x1.board.board[0][1].is_bomb()
    assert game_2x1.state == GameState.WIN


def test_game_check_win_win(game_2x1: Game, win_board_2x1: Board):
    game_2x1.board = win_board_2x1
    game_2x1.check_win()
    assert game_2x1.state == GameState.WIN


def test_game_check_win_not_win(game_2x1: Game, win_board_2x1: Board):
    game_2x1.check_win()
    assert game_2x1.state == GameState.PLAYING


def test_game_state_data(game_2x1, state_data_2x1: dict):
    assert game_2x1.state_data() == state_data_2x1


def test_game_display_state(state_data_2x1: dict, capfd):
    Game.display_state(state_data_2x1)
    out, _ = capfd.readouterr()
    print(r'{}'.format(out))
    assert out == "  0 \n0 _ _ \n\nplaying | Bombs: 1 | Flags: 0 | Revealed: 0\n"

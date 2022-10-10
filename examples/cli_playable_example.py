from typing import Callable
from minesweeper_sandbox import Game, GameAction, GameDifficulty, GameState

def validate_input(prompt: str, validation_fn: Callable[[str], bool], error_message: str = "Invalid Input") -> any:
    user_input = input(prompt)
    while not validation_fn(user_input):
        print(error_message)
        user_input = input(prompt)

    return user_input

def main():
    g = Game(difficulty=GameDifficulty.BEGINNER)
    game_over = False
    print("")

    while not game_over:
        Game.display_state(g.state_data())
        x = validate_input(
            prompt="\n(x) > ",
            validation_fn=lambda x: x.isdigit() and int(x) >=0 and int(x) < GameDifficulty.BEGINNER.value.width,
            error_message=f"X must be an integer between 0 and {GameDifficulty.BEGINNER.value.width-1}."
        )
        y = validate_input(
            prompt="\n(y) > ",
            validation_fn=lambda y: y.isdigit() and int(y) >=0 and int(y) < GameDifficulty.BEGINNER.value.height,
            error_message=f"Y must be an integer between 0 and {GameDifficulty.BEGINNER.value.height-1}."
        )
        a = validate_input(
            prompt=f"\nChoose an action on space ({x}, {y})\n(r)eveal, (f)lag > ",
            validation_fn=lambda a: a.lower() in ["r", "f", "reveal", "flag"],
            error_message="Invalid action."
        )
        print("")
        a = GameAction.FLAG if a == "f" else GameAction.REVEAL
        state = g.action(action=a, x=int(x), y=int(y))
        if state == GameState.LOOSE:
            print("You loose!")
            game_over = True
        if state == GameState.WIN:
            print("You win!")
            game_over = True

    print("")
    Game.display_state(g.state_data())

if __name__ == "__main__":
    main()
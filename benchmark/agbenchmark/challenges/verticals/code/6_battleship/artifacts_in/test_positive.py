import string
from typing import Any, Dict, List, Optional, Tuple, Union

from abstract_class import ShipPlacement, Turn


def test_turns_and_results(
    battleship_game: Any, initialized_game_id: str
) -> None:
    turn = Turn(target={"row": 1, "column": "A"})
    response = battleship_game.create_turn(initialized_game_id, turn)

    assert response.result in ["hit", "miss"], f"Invalid result: {response.result}"
    if response.result == "hit":
        assert response.ship_type == "carrier", f"Invalid ship type: {response.ship_type}"
    game = battleship_game.get_game(initialized_game_id)
    assert turn in game.turns, f"Turn not found in game turns: {turn}"


def test_game_status_and_winner(battleship_game: Any) -> None:
    game_id = battleship_game.create_game()
    status = battleship_game.get_game_status(game_id)
    assert isinstance(status.is_game_over, bool), f"Invalid is_game_over type: {type(status.is_game_over)}"
    if status.is_game_over:
        winner = battleship_game.get_winner(game_id)
        assert winner is not None, f"Winner is None: {winner}"


def test_delete_game(battleship_game: Any) -> None:
    game_id = battleship_game.create_game()
    battleship_game.delete_game(game_id)
    game = battleship_game.get_game(game_id)
    assert game is None, f"Game not deleted: {game}"


def test_ship_rotation(battleship_game: Any) -> None:
    game_id = battleship_game.create_game()
    placement_horizontal = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "B"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, placement_horizontal)
    placement_vertical = ShipPlacement(
        ship_type="cruiser", start={"row": 3, "column": "D"}, direction="vertical"
    )
    battleship_game.create_ship_placement(game_id, placement_vertical)
    game = battleship_game.get_game(game_id)
    assert placement_horizontal in game.ships, f"Horizontal placement not found in game ships: {placement_horizontal}"
    assert placement_vertical in game.ships, f"Vertical placement not found in game ships: {placement_vertical}"


def test_game_state_updates(battleship_game: Any, initialized_game_id: str) -> None:
    turn = Turn(target={"row": 3, "column": "A"})
    battleship_game.create_turn(initialized_game_id, turn)

    game = battleship_game.get_game(initialized_game_id)

    target_key = (3, ord("A") - ord("A"))
    assert target_key in game.board, f"Target key not found in game board: {target_key}"
    assert game.board[target_key] in ["hit", "miss"], f"Invalid board value: {game.board[target_key]}"


def test_ship_sinking_feedback(battleship_game: Any, initialized_game_id: str) -> None:
    hits = list(string.ascii_lowercase[:4])
    static_moves = [
        {"row": 1, "column": column}
        for column in list(string.ascii_uppercase[5:9])
    ]

    for index, hit in enumerate(hits):
        turn = Turn(target={"row": 2, "column": hit})
        response = battleship_game.create_turn(initialized_game_id, turn)
        assert response.ship_type == "battleship", f"Invalid ship type: {response.ship_type}"

        static_turn = Turn(target=static_moves[index])
        battleship_game.create_turn(initialized_game_id, static_turn)

    assert response.result == "sunk", f"Invalid result: {response.result}"


def test_restart_game(battleship_game: Any) -> None:
    game_id = battleship_game.create_game()
    battleship_game.delete_game(game_id)
    game_id = battleship_game.create_game()  # Use the returned game_id after recreating the game
    game = battleship_game.get_game(game_id)
    assert game is not None, f"Game is None: {game}"


def test_ship_edge_overlapping(battleship_game: Any) -> None:
    game_id = battleship_game.create_game()

    first_ship = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "A"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, first_ship)

    next_ship = ShipPlacement(
        ship_type="cruiser", start={"row": 1, "column": "E"}, direction="horizontal"
    )
    battleship_game.create_ship_placement(game_id, next_ship)

    game = battleship_game.get_game(game_id)
    assert first_ship in game.ships, f"First ship not found in game ships: {first_ship}"
    assert next_ship in game.ships, f"

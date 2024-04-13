import pytest
from abstract_class import ShipPlacement, Turn
from battleship import Battleship


@pytest.fixture
def battleship_game():
    return Battleship()


@pytest.fixture
def initialize_game(battleship_game):
    def game_initializer(ship_placements=None):
        # Create a game instance
        game_id = battleship_game.create_game()

        if not ship_placements:
            # Place all the ships using battleship_game's methods
            ship_placements = [
                ShipPlacement(
                    ship_type="carrier", start={"row": 1, "column": "A"}, direction="horizontal"
                ),
                ShipPlacement(
                    ship_type="battleship",
                    start={"row": 2, "column": "A"},
                    direction="horizontal",
                ),
                ShipPlacement(
                    ship_type="cruiser", start={"row": 3, "column": "A"}, direction="horizontal"
                ),
                ShipPlacement(
                    ship_type="submarine",
                    start={"row": 4, "column": "A"},
                    direction="horizontal",
              

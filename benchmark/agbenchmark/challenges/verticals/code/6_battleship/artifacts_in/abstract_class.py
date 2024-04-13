from abc import ABC, abstractmethod
from typing import (
    Any,
    ClassVar,
    Dict,
    Final,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, validator

T = TypeVar("T")


class ShipPlacement(BaseModel):
    ship_type: str
    start: Dict[str, int]  # {"row": int, "column": int}
    direction: str

    @validator("start")
    def validate_start(cls, start):
        row, column = start.get("row"), start.get("column")

        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")

        if not (1 <= column <= 10):
            raise ValueError("Column must be between 1 and 10 inclusive.")

        return start


class Turn(BaseModel):
    target: Dict[str, int]  # {"row": int, "column": int}


class TurnResponse(BaseModel):
    result: str
    ship_type: Optional[str]


class GameStatus(BaseModel):
    is_game_over: bool
    winner: Optional[str]


class Game(BaseModel):
    game_id: str
    players: List[str]
    board: Dict[str, str]  # This could represent the state of the game board, you might need to flesh this out further
    ships: List[ShipPlacement]
    turns: List[Turn]


class AbstractBattleship(ABC):
    SHIP_LENGTHS: ClassVar[Dict[str, int]] = {
        "carrier": 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2,
    }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, method in cls.__abstractmethods__.items():
            if not isinstance(getattr(cls, name), classmethod):
                raise NotImplementedError(f"{name} must be implemented as a classmethod")

    @classmethod
    @abstractmethod
    def create_ship_placement(cls, game_id: str, placement: ShipPlacement) -> None:
        """
        Place a ship on the grid.
        """
        ...

    @classmethod
    @abstractmethod
    def create_turn(cls, game_id: str, turn: Turn) -> TurnResponse:
        """
        Players take turns to target a grid cell.
        """
        ...

    @classmethod
    @abstractmethod
    def get_game_status(cls, game_id: str) -> GameStatus:
        """
        Check if the game is over and get the winner if there's one.
        """
        ...

    @classmethod
    @abstractmethod
    def get_winner(cls, game_id: str) -> str:
        """
        Get the winner of the game.
        """
        ...

    @property
    @abstractmethod
    def game(self) -> Game:
        """
        Retrieve the state of the game.
        """
        ...

    @classmethod
    @abstractmethod
    def delete_game(cls, game_id: str) -> None:
        """
        Delete a game given its ID.
        """
        ...

    @classmethod
    @abstractmethod


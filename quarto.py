"""FastAPI backend for the Quarto Game project.

This module contains:
- game logic for Player vs Computer mode,
- game logic for Player vs Player mode,
- request models for API communication,
- FastAPI endpoints used by the frontend.
"""

from uuid import uuid4
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


WINNING_LINES: dict[int, list[int]] = {
    1: [11, 12, 13, 14],
    2: [21, 22, 23, 24],
    3: [31, 32, 33, 34],
    4: [41, 42, 43, 44],
    5: [11, 21, 31, 41],
    6: [12, 22, 32, 42],
    7: [13, 23, 33, 43],
    8: [14, 24, 34, 44],
    9: [11, 22, 33, 44],
    10: [14, 23, 32, 41],
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]


class QuartoGame:
    """Represents one Player vs Computer Quarto game session.

    The class stores the current board, free stones, game status,
    information about the stone currently assigned to the player,
    and the last move made during the game.
    """

    def __init__(self) -> None:
        """Initialize a new game with a clean board and full stone set."""
        self.board = self.create_empty_board()
        self.free_stones = self.generate_stones()
        self.status = "playing"
        self.stone_for_player = None
        self.last_move = None
        self.lines_with_fields = WINNING_LINES

    """ METHODS TO CREATE GAME """

    def generate_stones(self) -> list[str]:
        """Generate all 16 unique stones represented as 4-bit binary strings.

        Returns:
            list[str]: List of stones from ``0000`` to ``1111``.
        """
        stones = set()

        for number in range(16):
            binary = format(number, "04b")
            stones.add(binary)

        return list(stones)

    def create_empty_board(self) -> dict[int, str | None]:
        """Create a 4x4 board with all fields initialized to ``None``.

        The board uses keys such as 11, 12, 13 ... 44,
        where the first digit is the row and the second digit is the column.

        Returns:
            dict[int, str | None]: Empty board structure.
        """
        fields: dict[int, str | None] = {}
        for r in range(1, 5):
            for c in range(1, 5):
                field = (r * 10) + c
                fields[field] = None
        return fields

    def create_new_game_state(self) -> dict:
        """Create a fresh serializable game-state snapshot.

        This helper returns the default state structure that can be used
        for debugging, comparison, or future reset functionality.

        Returns:
            dict: New game state with default values.
        """
        return {
            "board": self.create_empty_board(),
            "free_stones": [
                "0000", "0001", "0010", "0011",
                "0100", "0101", "0110", "0111",
                "1000", "1001", "1010", "1011",
                "1100", "1101", "1110", "1111",
            ],
            "remaining_stones": 16,
            "status": "playing",
            "stone_for_player": None,
            "last_move": None,
        }

    def create_new_game_id(self) -> str:
        """Generate a unique identifier for a new game session.

        Returns:
            str: UUID string used as game ID.
        """
        return str(uuid4())

    def check_game_state(self) -> bool:
        """Check whether the current board contains a winning line.

        The method checks all rows, columns, and diagonals. A line is winning
        only when all four fields are occupied and all four stones share
        the same value on at least one attribute index.

        Returns:
            bool: ``True`` if a winning line exists, otherwise ``False``.
        """
        for _, fields in self.lines_with_fields.items():
            if (
                self.board[fields[0]]
                and self.board[fields[1]]
                and self.board[fields[2]]
                and self.board[fields[3]]
            ):
                for i in range(4):
                    if (
                        self.board[fields[0]][i]
                        == self.board[fields[1]][i]
                        == self.board[fields[2]][i]
                        == self.board[fields[3]][i]
                    ):
                        return True

        return False

    def _build_state(self, extra: dict | None = None) -> dict:
        """Build a serializable state dictionary shared by API responses.

        Args:
            extra (dict | None): Optional extra values for a specific game mode.

        Returns:
            dict: Current game state.
        """
        state = {
            "board": self.board,
            "free_stones": list(self.free_stones),
            "remaining_stones": len(self.free_stones),
            "status": self.status,
            "last_move": self.last_move,
        }

        if extra:
            state.update(extra)

        return state

    def _update_status_after_placement(self, has_won: bool, winner_status: str) -> None:
        """Update the overall game status after a stone has been placed.

        Args:
            has_won (bool): Result of the winning-condition check.
            winner_status (str): Status value to set when the player wins.
        """
        if has_won:
            self.status = winner_status
        elif not self.free_stones:
            self.status = "no winner"
        else:
            self.status = "playing"

    def get_state(self) -> dict:
        """Return the current state of the Player vs Computer game.

        Returns:
            dict: Current game data sent back to the client.
        """
        return self._build_state({"stone_for_player": self.stone_for_player})

    """ METHODS TO MAKE First part of game where Players gives stone to computer and computer place it randomly and after give random stone to player"""

    def take_stone(self, input_stone: BaseModel) -> None:
        """Remove the selected stone from the pool of free stones.

        Args:
            input_stone (BaseModel): Request object with ``chosen_stone``.

        Raises:
            ValueError: If the selected stone is not available.
        """
        stone = input_stone.chosen_stone

        if stone not in self.free_stones:
            raise ValueError("Stone not available.")

        self.free_stones.remove(stone)

    def open_fields(self) -> list[int]:
        """Return a list of currently empty board fields.

        Returns:
            list[int]: Field identifiers that are not occupied yet.
        """
        return [field for field, stone in self.board.items() if stone is None]

    def random_place(self, input_stone: BaseModel) -> dict:
        """Place the given stone on a random free field.

        Args:
            input_stone (BaseModel): Request object with ``chosen_stone``.

        Returns:
            dict: Dictionary describing the computer move.
        """
        stone = input_stone.chosen_stone
        free_fields = self.open_fields()
        random_field = random.choice(free_fields)
        self.board[random_field] = stone
        placing_stone_dictionary_by_computer: dict = {"stone": stone, "field": random_field}
        return placing_stone_dictionary_by_computer

    def random_take(self) -> dict:
        """Randomly choose one free stone for the player and remove it.

        Returns:
            dict: Dictionary in format ``{"chosen_stone": "...."}``.

        Raises:
            ValueError: If there are no stones left.
        """
        if not self.free_stones:
            raise ValueError("No stones left to take.")

        random_stone = random.choice(list(self.free_stones))
        chosen_stone = {"chosen_stone": random_stone}
        self.free_stones.remove(random_stone)
        return chosen_stone

    def give_stone_to_computer_move(self, request: BaseModel) -> None:
        """Execute the full server turn after player gives a stone to the computer.

        Server actions:
        - remove selected stone from ``free_stones``,
        - place the stone randomly on the board,
        - check whether the computer has won,
        - if game continues, choose a random stone for the player.

        Args:
            request (BaseModel): ``{"chosen_stone": "1111"}``
        """
        self.take_stone(request)
        placing_stone_by_computer: dict = self.random_place(request)
        has_computer_won = self.check_game_state()

        if has_computer_won:
            self.status = "computer wins"
            self.stone_for_player = None
        else:
            self.status = "playing"
            self.stone_for_player = self.random_take()

        self.last_move = {
            "player_action": "gave_stone",
            "computer_move": placing_stone_by_computer,
        }

    def place_stone(self, request: BaseModel) -> None:
        """Place the player's assigned stone on the selected board field.

        Server actions:
        - place stone on the board,
        - check whether the player has won,
        - update game status,
        - clear ``stone_for_player`` because the move has been completed.

        Args:
            request (BaseModel):
                ``{"stone": "1010", "field": 12}``
        """
        stone = request.stone
        field = request.field
        self.board[field] = stone
        has_player_won = self.check_game_state()
        self._update_status_after_placement(has_player_won, "player wins")
        self.stone_for_player = None
        self.last_move = {"player_move": request}


class QuartoGamePvP(QuartoGame):
    """Represents one Player vs Player Quarto game session."""

    def __init__(self) -> None:
        """Initialize a new PvP game and track each player's current action."""
        super().__init__()
        self.player1_action = None
        self.player2_action = None

    def get_state(self) -> dict:
        """Return the current state of the Player vs Player game.

        Returns:
            dict: Current PvP game data sent back to the client.
        """
        return self._build_state(
            {
                "player1_action": self.player1_action,
                "player2_action": self.player2_action,
            }
        )

    def place_stone(self, request: BaseModel) -> None:
        """Process one PvP move and update game state.

        The method reads player actions from the request, places the stone,
        removes it from free stones, checks for a winner, and updates
        the overall game status.

        Args:
            request (BaseModel):
                {
                    "stone": "0100",
                    "field": 23,
                    "player1_action": "placed_stone",
                    "player2_action": "gave_stone"
                }
        """
        self.last_move = request
        self.player1_action = request.player1_action
        self.player2_action = request.player2_action
        stone, field = request.stone, request.field

        self.board[field] = stone
        self.free_stones.remove(stone)

        if self.player1_action == "placed_stone":
            has_player1_won = self.check_game_state()
            self._update_status_after_placement(has_player1_won, "player1 wins")
            self.last_move = {"player1_move": request}
        else:
            has_player2_won = self.check_game_state()
            self._update_status_after_placement(has_player2_won, "player2 wins")
            self.last_move = {"player2_move": request}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games: dict[str, QuartoGame] = {}


class GiveStoneRequest(BaseModel):
    """Request body for giving a stone to the computer."""

    chosen_stone: str


class PlaceStoneRequest(BaseModel):
    """Request body for placing a stone in Player vs Computer mode."""

    stone: str
    field: int


class PlaceStoneRequestPvP(BaseModel):
    """Request body for placing a stone in Player vs Player mode."""

    stone: str
    field: int
    player1_action: str
    player2_action: str


@app.post("/games")
def create_game() -> dict:
    """Create a new Player vs Computer game and return its initial state."""
    print("1. endpoint start")
    game = QuartoGame()
    game_id = game.create_new_game_id()

    games[game_id] = game

    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


@app.get("/games/{game_id}")
def get_game(game_id: str) -> dict:
    """Return the current state of an existing Player vs Computer game.

    Args:
        game_id (str): Unique identifier of the requested game.

    Raises:
        HTTPException: If the game does not exist.

    Returns:
        dict: API response with current game state.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    print(game)
    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


@app.post("/games/{game_id}/give-stone-to-computer")
def give_stone_to_computer(game_id: str, request: GiveStoneRequest) -> dict:
    """Process the move where the player gives a stone to the computer.

    Args:
        game_id (str): Unique identifier of the requested game.
        request (GiveStoneRequest): Selected stone sent by the client.

    Raises:
        HTTPException: If the game does not exist.

    Returns:
        dict: API response with updated game state.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    game.give_stone_to_computer_move(request)

    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


@app.post("/games/{game_id}/place-stone")
def place_stone(game_id: str, request: PlaceStoneRequest) -> dict:
    """Process the move where the player places the assigned stone.

    Args:
        game_id (str): Unique identifier of the requested game.
        request (PlaceStoneRequest): Stone and target field.

    Raises:
        HTTPException: If the game does not exist.

    Returns:
        dict: API response with updated game state.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    game.place_stone(request)

    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


""" PvP Endpoints and FastAPI """


@app.post("/gamespvp")
def create_game_pvp() -> dict:
    """Create a new Player vs Player game and return its initial state."""
    print("1. endpoint start")
    game = QuartoGamePvP()
    print(game.__dict__)
    game_id = game.create_new_game_id()

    games[game_id] = game

    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


@app.get("/gamespvp/{game_id}")
def get_game_pvp(game_id: str) -> dict:
    """Return the current state of an existing Player vs Player game.

    Args:
        game_id (str): Unique identifier of the requested game.

    Raises:
        HTTPException: If the game does not exist.

    Returns:
        dict: API response with current PvP game state.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    print(game)
    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }


@app.post("/gamespvp/{game_id}/place-stone")
def place_stone_pvp(game_id: str, request: PlaceStoneRequestPvP) -> dict:
    """Process one PvP move where one player places the selected stone.

    Args:
        game_id (str): Unique identifier of the requested game.
        request (PlaceStoneRequestPvP): Stone, field, and action metadata.

    Raises:
        HTTPException: If the game does not exist.

    Returns:
        dict: API response with updated PvP game state.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    game.place_stone(request)

    return {
        "success": True,
        "game_id": game_id,
        "state": game.get_state(),
    }

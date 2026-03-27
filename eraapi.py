from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel



app = FastAPI()

games: dict[str, dict] = {}

class GiveStoneRequest(BaseModel):
    chosen_stone: str


class PlaceStoneRequest(BaseModel):
    stone: str
    field: int



def create_empty_board() -> dict[str, str | None]:
    board = {}
    for row in range(1, 5):
        for col in range(1, 5):
            field = f"{row}{col}"
            board[field] = None
    return board




def create_new_game_state() -> dict:
    return {
        "board": create_empty_board(),
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

@app.post("/games")
def create_game():
    game_id = str(uuid4())
    state = create_new_game_state()
    games[game_id] = state

    return {
        "success": True,
        "game_id": game_id,
        "state": state,
    }
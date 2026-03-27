
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None



inventory = {
    1: {
        "name": "beer",
        "price": 1.5,
        "brand": "Pilsner"
    },

    2: {
        "name": "Coca-cola",
        "price": 1.5
    },

    3: {
        "name": "Bacon",
        "price": 2.5
    },
}


@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    return inventory[item_id]


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return{"Error": "Item ID already exists"}
    inventory[item_id] = item
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        return{"Error": "Item ID not exists"}
    inventory.pop(item_id)

@app.put("/update-item/{item_id}")
def update_item(item_id: int, update_item: UpdateItem):
    if item_id not in inventory:
        return{"Error": "Item ID not exists"}
    
    inventory[item_id].update(update_item.model_dump(exclude_unset=True))
    return inventory[item_id]




import json
from eragame import EraGame

# app = FastAPI()
saved_games: dict[str, dict] = {}



class GiveStoneRequest(BaseModel):
    chosen_stone: str

class PlaceStoneRequest(BaseModel):
    stone: str
    field: int




@app.post("/games")
def create_game():
    print("1. endpoint start")

    game = EraGame()
    
    print("2. game created:", game)

    print("3. game_id:", game.game_id)
    print("4. game_state:", game.game_state)

    saved_games[game.game_id] = game.game_state
    print("5. saved into games")
    print(saved_games)

    return {
        "success": True,
        "game_id": game.game_id,
        "state": game.game_state,
    }






@app.get("/games/{game_id}")
def get_game(game_id: str):
    game = saved_games.get(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return {
        "success": True,
        "game_id": game_id,
        "state": game,
    }




# Server actions: 
# - remove stone from free_stones 
# - computer places stone 
# - check game status 
# - if playing → computer chooses new stone for player


@app.post("/games/{game_id}/give-stone")
def give_stone(game_id: str, request: GiveStoneRequest):
    game = EraGame()
    game.game_id = game_id
    game.game_state = saved_games[game_id]
    game.stones.take_stone(request)
    stone_randomly_placed: dict = game.board.random_place(request)
    

    # game.game_over = game.check_game()
    # if game.game_over:
    #     status_messasage: dict = {"status": "computer wins"}
    #     self.communication.announcing_game_status_json(status_messasage)
    #     break
    #  else:
    #     status_messasage: dict = {"status": "playing"}
    #     self.communication.announcing_game_status_json(status_messasage)


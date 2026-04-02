from uuid import uuid4
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class QuartoGame:
    
    def __init__(self):
        self.board = self.create_empty_board()
        self.free_stones = self.generate_stones()
        self.status = "playing"
        self.stone_for_player = None
        self.last_move = None
    
        # AUXILIARY dict. for method check_game_state
        self.lines_with_fields: dict = {
                 1 : [11,12,13,14], 
                 2 : [21,22,23,24],
                 3 : [31,32,33,34],
                 4 : [41,42,43,44],
                 5 : [11,21,31,41],
                 6 : [12,22,32,42],
                 7 : [13,23,33,43],
                 8 : [14,24,34,44],
                 9 : [11,22,33,44],
                 10 : [14,23,32,41]
                 }
   
   
   
   
   
    """ METHODS TO CREATE GAME """
    
    def generate_stones(self) -> list[str]:
        """
        Generates all 16 unique 4-bit stones. (converts 0..15 into 4-bit binary)
        """
        stones = set()

        for number in range(16):
            binary = format(number, "04b")  
            stones.add(binary)

        return list(stones)
    
    
    
    def create_empty_board(self) -> dict[int, str | None]:
        fields: dict[int, str | None] = {}
        for r in range(1, 5):
            for c in range(1, 5):
                field = (r * 10) + c
                fields[field] = None
        return fields
    
    def create_new_game_state(self) -> dict:
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
        return str(uuid4())
    

    def check_game_state(self) -> bool:
        """
        This method checks whether, after being last stone placed, the winning conditions were met.
        First it check IF row / column / diagonal line of four fields is fully field each one with a stone,
        THEN IF all four stones have same value (0 or 1) on the same index.
        
        Returns:
        IF all these conditions are met, return TRUE value, ELSE return FALSE
        """

        for line, fields in self.lines_with_fields.items():
            if self.board[fields[0]] and self.board[fields[1]] and self.board[fields[2]] and self.board[fields[3]]:
                
                for i in range(4):
                    if self.board[fields[0]][i] == self.board[fields[1]][i] == self.board[fields[2]][i] == self.board[fields[3]][i]:
                        return True      
            
        return False






    def get_state(self) -> dict:
        return {
            "board": self.board,
            "free_stones": list(self.free_stones),
            "remaining_stones": len(self.free_stones),
            "status": self.status,
            "stone_for_player": self.stone_for_player,
            "last_move": self.last_move,
        }
    








    """ METHODS TO MAKE First part of game where Players gives stone to computer and computer place it randomly and after give random stone to player"""
    

    def take_stone(self, input_stone: dict) -> None:
        """
        Removes stone from free stones if available.
        Raises ValueError if stone does not exist.
        """
        stone = input_stone.chosen_stone
        

        if stone not in self.free_stones:
            raise ValueError("Stone not available.")
        
        self.free_stones.remove(stone)
    
    
    def open_fields(self) -> list[int]:
        return [field for field, stone in self.board.items() if stone is None]

    def random_place(self, input_stone: dict) -> dict: 
        stone = input_stone.chosen_stone
        free_fields = self.open_fields()
        random_field = random.choice(free_fields)
        self.board[random_field] = stone
        placing_stone_dictionary_by_computer: dict = {"stone":stone, "field": random_field}
        return placing_stone_dictionary_by_computer

    def random_take(self) -> dict:
        """
        Converst free_stones(set) to free_stones(list)
        Randomly selects a stone from free stones,
        removes it, and returns it.
        Raises ValueError if no stones are left.
        """
        if not self.free_stones:
            raise ValueError("No stones left to take.")

        random_stone = random.choice(list(self.free_stones))
        chosen_stone = {"chosen_stone": random_stone}
        self.free_stones.remove(random_stone)
        return chosen_stone




    def give_stone_to_computer_move(self, request: BaseModel) -> None:
        """
        Args:
            request (dict): {"chosen_stone": "1111"}
        
        # Server actions: 
        # - remove stone from free_stones 
        # - computer places stone 
        # - check game status 
        # - if playing → computer chooses new stone for player
    
        """
        self.take_stone(request)
        placing_stone_by_computer: dict = self.random_place(request)
        hasComputer_won = self.check_game_state()
        if hasComputer_won:
            self.status = "computer wins"
            self.stone_for_player  = None 
        else:
             self.status = "playing"
             self.stone_for_player = self.random_take()
        self.last_move = {"player_action": "gave_stone",
                          "compute move": placing_stone_by_computer}
    

    """ METHOD TO place stone from computer by player 
    
            # Server actions:
            # - place stone on board
            # - check game status 
            # Request:
            {
            "stone": "1010",
            "field": 12
            }   
            # """

        
    def place_stone(self, request: BaseModel) -> None:
        """
        Places a stone on the given field.
        """
        stone = request.stone
        field = request.field
        self.free_stones.remove(stone)
        self.board[field] = stone
        hasPlayer_won = self.check_game_state()
        if hasPlayer_won:
            self.status = "Player wins"
            
        else:
            self.status = "playing"
        self.stone_for_player =  None
        self.last_move ={"player_move": request 
                                        }

    


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games: dict[str, QuartoGame] = {}

class GiveStoneRequest(BaseModel):
    chosen_stone: str


class PlaceStoneRequest(BaseModel):
    stone: str
    field: int



@app.post("/games")
def create_game():
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
def get_game(game_id: str):

    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    print(game)
    return {
        "success": True,
        "game_id": game_id,
        "state":  game.get_state(),
    }


@app.post("/games/{game_id}/give-stone-to-computer")
def give_stone_to_computer(game_id: str, request: GiveStoneRequest):
    
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id] 
    game.give_stone_to_computer_move(request)
    
    return {
        "success": True,
        "game_id": game_id,
        "state":  game.get_state(),
    }



@app.post("/games/{game_id}/place-stone") 
def place_stone(game_id: str, request: PlaceStoneRequest):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id] 
    game.place_stone(request)
    
    return {
        "success": True,
        "game_id": game_id,
        "state":  game.get_state(),
    }
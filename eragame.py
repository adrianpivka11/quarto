from Board import Board
from Stones import Stones
from Communication import Communication
import json

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel






class EraGame:
    
    def __init__(self):
        self.board = Board()
        self.stones = Stones()
        self.communication = Communication()
        
        self.game_id = str(uuid4())
        self.game_state = {
        "board": self.board._create_empty_fields(),
        "free_stones": self.stones._generate_stones(),
        "remaining_stones": 16,
        "status": "playing",
        "stone_for_player": None,
        "last_move": None,
    }


        self.game_over = False
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
    
    def get_state(self) -> dict:
        return {
            "board": self.board.fields,
            "free_stones": list(self.stones.free_stones),
            "remaining_stones": len(self.stones.free_stones),
            "status": self.status,
            "stone_for_player": self.stone_for_player,
            "last_move": self.last_move,
        }





    def check_empty_stones(self) -> bool:
        """
        Check if 'bucket' (set) with stones is not empty. If so, end the game cycle and announce game status 'no winner'
        """
        if not self.stones.free_stones:
                print("No winner")
                return Tru




    def check_game(self) -> bool:
        """
        This method checks whether, after being last stone placed, the winning conditions were met.
       
            First it check IF row / column / diagonal line of four fields is fully field each one with a stone,
                THEN IF all four stones have same value (0 or 1) on the same index.
        Returns:
            IF all these conditions are met, return TRUE value, ELSE return FALSE
        """

        for line, fields in self.lines_with_fields.items():
            if self.board.fields[fields[0]] and self.board.fields[fields[1]] and self.board.fields[fields[2]] and self.board.fields[fields[3]]:
                
                for i in range(4):
                    if self.board.fields[fields[0]][i] == self.board.fields[fields[1]][i] == self.board.fields[fields[2]][i] == self.board.fields[fields[3]][i]:
                        return True      
            
        return False


    def run_era_game(self) -> None:
       
        """
        Main game cycle:
        1. Check if 'bucket' with stones is not empty. If so, end the game cycle and announce game status 'no winner'
        2. Player gives a stone to computer by JSON request
        3. Computer places the stone randomly and JSON response about it is being sent.
        4. Check game status, announcing game status by JSON response (computer wins | playing) If computer wins, end cycle.
        5. Check if 'bucket' with stones is not empty. If so, end the game cycle and announce game status 'no winner'
        6. Computer gives random stone to player by JSON response
        7. Player places the stone by JSON request
        8. Check game status, announcing game status by JSON response (player wins | playing). If player wins, end cycle.
        9. Repeat cycle

        """ 

        while not self.game_over:
            

            """" 1st phase Player gives stone, Computer randomly places it"""
            
            if self.check_empty_stones():
                status_messasage: dict = {"status": "no winner"}
                self.communication.announcing_game_status_json(status_messasage)
                break 
            stone_for_computer: dict = self.communication.request_json()
            self.stones.take_stone(stone_for_computer)
            stone_randomly_placed: dict = self.board.random_place(stone_for_computer)
            self.communication.respond_json(stone_randomly_placed)
    

            self.game_over = self.check_game()
            if self.game_over:
                status_messasage: dict = {"status": "computer wins"}
                self.communication.announcing_game_status_json(status_messasage)
                break
            else:
                status_messasage: dict = {"status": "playing"}
                self.communication.announcing_game_status_json(status_messasage)


            """" 2nd phase Computer gives random stone, Player places it """
            
            if self.check_empty_stones():
                status_messasage: dict = {"status": "no winner"}
                self.communication.announcing_game_status_json(status_messasage)
                break
            stone_for_player: dict = self.stones.random_take()
            self.communication.respond_json(stone_for_player)
            field_to_place_by_player: dict = self.communication.request_json()
            self.board.place(stone_for_player, field_to_place_by_player)
            

            self.game_over = self.check_game()
            if self.game_over:
                status_messasage: dict = {"status": "player wins"}
                self.communication.announcing_game_status_json(status_messasage)
                break
            else:
                status_messasage: dict = {"status": "playing"}
                self.communication.announcing_game_status_json(status_messasage)



"VYTVORENIE APPky pre API REQUEST RESPONSE CYCLE"




if __name__ == "__main__":
    eragame = EraGame()
    print(eragame.game_state)
    b = eragame.game_state
    json_type = json.dumps(b)
    print(json_type)
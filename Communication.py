import sys
import json


class Communication:
    

    def request_json(self) -> dict :
        """
        get input by JSON request and transofrm it into python dict
        returns python dict
        """
        stone_input = sys.stdin.readline()

        return json.loads(stone_input)
    

    def respond_json(self, placing_stone_dictionary : dict) -> None:
        """
        Args:
        python dict

        Returns:
        JSON response
        """
        message = json.dumps(placing_stone_dictionary)
        print(message)
        sys.stdout.flush()


    def announcing_game_status_json (self, status_messasage : dict) -> None:
        """
        Args:
        python dict

        Returns:
        JSON response
        """
        message = json.dumps(status_messasage)
        print(message)
        sys.stdout.flush()
        
          
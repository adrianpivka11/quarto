import random


"""
create (initialize) variable available_stones by using JSON data type technology - with ID and 4 different characteristics e.g. "0100" so that they can be taken by player / computer and placed on board.
available_stones will have 16 stones in total.
If the stone is taken by player. Delete the stone from the available_stones.  
"""

class Stones:
    """
    Manages all free stones in the ERA Game.

    Each stone is represented as a 4-bit string, e.g. "0101".
    There are 16 unique stones (2^4 combinations).
    """

    def __init__(self):
        self.free_stones = self._generate_stones()

    def _generate_stones(self) -> list[str]:
        """
        Generates all 16 unique 4-bit stones. (converts 0..15 into 4-bit binary)
        """
        stones = set()

        for number in range(16):
            binary = format(number, "04b")  
            stones.add(binary)

        return list(stones)

    def get_all(self) -> set[str]:
        """
        Returns all currently available stones.
        """
        return self.free_stones

    def take_stone(self, input_stone: dict) -> None:
        """
        Removes stone from free stones if available.
        Raises ValueError if stone does not exist.
        """
        stone = input_stone["chosen_stone"]
        

        if stone not in self.free_stones:
            raise ValueError("Stone not available.")
        
        self.free_stones.remove(stone)

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
        
    

    def count(self) -> int:
        """
        Returns number of remaining stones.
        """
        return len(self.free_stones)
    
    


if __name__ == "__main__":
    available_stones = Stones()
    print (type(available_stones._generate_stones()))
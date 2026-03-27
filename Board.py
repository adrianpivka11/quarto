import random



class Board:
    """
    Represents a 4x4 ERA Game board.

    Fields are identified by two-digit numbers:
    11, 12, 13, 14,
    21, 22, 23, 24,
    31, 32, 33, 34,
    41, 42, 43, 44

    Each field holds either None (empty) or a stone string like "0101".
    """

    def __init__(self) -> None:
        self.fields: dict[int, str | None] = self._create_empty_fields()

    def _create_empty_fields(self) -> dict[int, str | None]:
        fields: dict[int, str | None] = {}
        for r in range(1, 5):
            for c in range(1, 5):
                field = (r * 10) + c
                fields[field] = None
        return fields

    def is_valid_field(self, field: int) -> bool:
        return field in self.fields

    def is_empty(self, field: int) -> bool:
        if not self.is_valid_field(field):
            raise ValueError("Invalid field.")
        return self.fields[field] is None

    def open_fields(self) -> list[int]:
        return [field for field, stone in self.fields.items() if stone is None]

    def is_full(self) -> bool:
        return all(stone is not None for stone in self.fields.values())

    def place(self, input_stone: dict, input_field: dict) -> None:
        """
        Places a stone on the given field.
        Raises ValueError if the field is invalid or already occupied.
        """
        stone = input_stone["chosen_stone"]
        field = input_field["field"]
        if not self.is_valid_field(field):
            raise ValueError("Invalid field.")
        if self.fields[field] is not None:
            raise ValueError("Field already occupied.")
        self.fields[field] = stone
    
    def random_place(self, input_stone: dict) -> dict: 
        stone = input_stone["chosen_stone"]
        free_fields = self.open_fields()
        random_field = random.choice(free_fields)
        self.fields[random_field] = stone
        placing_stone_dictionary: dict = {r"stone":stone, "field": random_field}
        return placing_stone_dictionary

    def print_actual_fields(self) -> None:
        print(self.fields)



if __name__ == "__main__":
    board = Board()
    print (type(board._create_empty_fields()))
    print (board._create_empty_fields())
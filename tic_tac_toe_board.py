import json
from dataclasses import dataclass, field

@dataclass
class TicTacToeBoard:
    state: str = "is playing"
    player_turn: str = "x"
    position: list = field(default_factory=lambda: ["", "", "", "", "", "", "", "", ""])

    def check_winner(self):
        for i in range(0, 9, 3):
            if self.position[i] == self.position[i + 1] == self.position[i + 2] != "":
                return True
        for i in range(3):
            if self.position[i] == self.position[i + 3] == self.position[i + 6] != "":
                return True
        if self.position[0] == self.position[4] == self.position[8] != "":
            return True
        if self.position[2] == self.position[4] == self.position[6] != "":
            return True
        return False
    
    def check_draw(self):
        if len(list(filter(lambda x: x == "", self.position))) == 0 and not self.check_winner():
            return True
        return False
        
    def switch_turn(self):
        self.player_turn = "o" if self.player_turn == "x" else "x"
    
    def is_my_turn(self, i_am: str) -> bool:
        return self.state == "is playing" and self.player_turn == i_am
    
    def make_move(self, index: int):
        if self.state == "is finished":
            return "The game is already finished."
        if not (0 <= index <= 8):
            return "Please input a valid index between 0 and 8."
        if self.position[index] != "":
            return "This position is already taken. Choose another position."
        self.position[index] = self.player_turn
        if self.check_draw():
            self.state = "is finished"
            return "It's a tie!"
        elif self.check_winner():
            self.state = "is finished"
            return f"Player {self.player_turn} wins!"
        else: 
            self.switch_turn()
            return f"Move successful! It's now {self.player_turn}'s turn."
        
    def serialize(self):
        return json.dumps({
            "state": self.state,
            "player_turn": self.player_turn,
            "position": self.position
        })
    
    def save_to_redis(self, redis_client, path, key):
        board_dict = {
            "state": self.state,
            "player_turn": self.player_turn,
            "position": self.position
        }
        redis_client.json().set(path, "$", board_dict)
    
    @classmethod
    def load_from_redis(cls, redis_client, path, key):
        data = redis_client.json().get(path, "$")
        if not data:
            return None
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        return cls(**data)
    
    def reset(self, redis_client, path, key):
        self.state = "is playing"
        self.player_turn = "x"
        self.position = ["", "", "", "", "", "", "", "", ""]
        self.save_to_redis(redis_client, path, key)




  
'''
board = TicTacToeBoard()
print(board.is_my_turn("x"))
print(board.make_move("8"))
'''



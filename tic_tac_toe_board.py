import json
from dataclasses import dataclass, field, asdict

@dataclass
class TicTacToeBoard:
    state: str = "is playing"
    player_turn: str = "x"
    position: list = field(default_factory=lambda: [""] * 9)

    def check_winner(self) -> bool:
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

    def check_draw(self) -> bool:
        return "" not in self.position and not self.check_winner()

    def switch_turn(self):
        self.player_turn = "o" if self.player_turn == "x" else "x"

    def is_my_turn(self, i_am: str) -> bool:
        return self.state == "is playing" and self.player_turn == i_am

    def make_move(self, index: int) -> dict:
        if self.state == "is finished":
            return {"success": False, "message": "The game is already finished."}

        if not (0 <= index <= 8):
            return {"success": False, "message": "Please input a valid index between 0 and 8."}

        if self.position[index] != "":
            return {"success": False, "message": "This position is already taken. Choose another position."}

        self.position[index] = self.player_turn

        if self.check_winner():
            self.state = "is finished"
            return {
                "success": True,
                "message": f"Player {self.player_turn} wins!",
                "board": self.to_dict()
            }

        if self.check_draw():
            self.state = "is finished"
            return {
                "success": True,
                "message": "It's a tie!",
                "board": self.to_dict()
            }

        self.switch_turn()
        return {
            "success": True,
            "message": f"Move successful! It's now {self.player_turn}'s turn.",
            "board": self.to_dict()
        }

    def to_dict(self) -> dict:
        return asdict(self)

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    async def save_to_redis(self, redis_client, path: str):
        await redis_client.json().set(path, "$", self.to_dict())

    @classmethod
    async def load_from_redis(cls, redis_client, path: str):
        data = await redis_client.json().get(path, "$")
        if not data:
            return None
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        return cls(**data)

    async def reset(self, redis_client, path: str):
        self.state = "is playing"
        self.player_turn = "x"
        self.position = [""] * 9
        await self.save_to_redis(redis_client, path)




'''
board = TicTacToeBoard()
print(board.is_my_turn("x"))
print(board.make_move("8"))
'''



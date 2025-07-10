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
        if len(list(filter(lambda x: x == "", self.position))) == 0 and self.check_winner() == False:
            return True
        else:
            return False
        
    def switch_turn(self):
        self.player_turn = "o" if self.player_turn == "x" else "x"
        
        
        
    
    def is_my_turn(self, turn: str) -> bool:
        return self.player_turn == turn
    
    def make_move(self, index: str):
        if self.state == "is finished":
            return "The game is already finished."
        try:
            index = int(index)
            if not (0 <= index <= 8):
                return "Please input a valid index between 0 and 8."
        except ValueError:
            return "Invalid input! Please input a number between 0 and 8."
        if self.position[index] != "":
            return "This position is already taken. Choose another position."
        self.position[index] = self.player_turn
        if self.check_draw() == True:
            self.state = "is finished"
            return f"It a tie!"
        elif self.check_winner() == True:
            self.state = "is finished"
            return f"Player {self.player_turn} wins!"
        else:
            self.switch_turn()
            return f"Move successful! It's now {self.player_turn}'s turn."
    
  
'''
board = TicTacToeBoard()
print(board.is_my_turn("x"))
print(board.make_move("8"))
'''
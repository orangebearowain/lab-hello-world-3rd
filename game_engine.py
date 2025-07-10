import tic_tac_toe_board 

def main():
    board = tic_tac_toe_board.TicTacToeBoard()

    player = input("Welcome to Tic-Tac-Toe! Do you want to be 'x' or 'o'? ").lower()
    while player not in ['x', 'o']:
        player = input("Invalid choice! Please choose 'x' or 'o': ").lower()

    board.player_turn = player 
    while board.state == "is playing":
        print("\nCurrent board:")
        print(board) 
        move = input(f"Player {board.player_turn}, enter your move (0-8): ")
        result = board.make_move(move)
        print(result) 
        
        if board.state == "is finished":
            print("\nFinal board:")
            print(board) 
            break 

if __name__ == "__main__":
    main()

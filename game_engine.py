import argparse
import tic_tac_toe_board
from redis import Redis

def main():
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe Game")
    parser.add_argument('--player', type=str, required=False, choices=['x', 'o'],
                        help="Choose 'x' or 'o' as the player symbol.")
    parser.add_argument('--reset', action='store_true',
                        help="Reset the game board before starting a new game.")
    
    args = parser.parse_args()
    

    r = Redis(
        host="abcde.com",
        port=2334223489509478592784,
        password="1234567890",
        db=1234567898765432
    )
    
    if args.reset:
        board = tic_tac_toe_board.TicTacToeBoard()
        board.reset(redis_client=r, path="game", key="tic_tac_toe_board")
        print("Board has been reset!")
        return
    
    board = tic_tac_toe_board.TicTacToeBoard.load_from_redis(r, path="game", key="tic_tac_toe_board")
    
    if not board:
        print("No saved game found, starting a new game!")
        board = tic_tac_toe_board.TicTacToeBoard()
        board.save_to_redis(r, path="game", key="tic_tac_toe_board")
    
    if board.is_my_turn(args.player):  
        print(f"\nWelcome to Tic-Tac-Toe! You are playing as '{args.player}'")
        print("\nCurrent board:")
        print(board)

        move = input(f"Player {board.player_turn}, enter your move (0-8): ")
        
        try:
            move = int(move)
        except ValueError:
            print("Invalid input! Please enter a number between 0 and 8.")
            return

        result = board.make_move(move)
        print(result)

        board.save_to_redis(r, path="game", key="tic_tac_toe_board")
        
        if board.state == "is finished":
            print("\nFinal board:")
            print(board)
    else:
        print(f"\nIt is not your turn yet! Current player is {board.player_turn}.")
        print("\nCurrent board:")
        print(board)

if __name__ == "__main__":
    main()

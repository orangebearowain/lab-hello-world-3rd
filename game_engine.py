import argparse
import asyncio
import redis.asyncio as redis  
import tic_tac_toe_board
import sys 


CHANNEL_NAME = 'ttt_game_state_changed'

# Handle the current board state, processing moves and checking for win/tie
async def handle_board_state(redis_client, i_am_playing: str):
    board = await tic_tac_toe_board.TicTacToeBoard.load_from_redis(redis_client, path="game")
    
    if not board:
        print("No saved game found!")
        return

    if board.state == "is finished":
        print("\nThe game has already ended!")
        print(f"Final board:")
        print(board)
        sys.exit()

    if board.is_my_turn(i_am_playing):
        print("\nCurrent board:")
        print(board)
        move = input(f"Player {board.player_turn}, enter your move (0-8): ")
        
        try:
            move = int(move)
        except ValueError:
            print("Invalid input! Please enter a number between 0 and 8.")
            return

        result = board.make_move(move)  # No 'await' here, since make_move is synchronous
        print(result)
        
        await board.save_to_redis(redis_client, path="game")
        await redis_client.publish(CHANNEL_NAME, "Board updated")

        if board.state == "is finished":
            if board.check_draw():  # No 'await' here
                print("The game has ended in a tie!")
                await redis_client.publish(CHANNEL_NAME, "Game has finished - Tie")  # Notify both terminals
                print(f"Final board:")
                print(board)
                sys.exit()

            elif board.check_winner():  # No 'await' here
                print(f"Player {board.player_turn} wins!")
                await redis_client.publish(CHANNEL_NAME, f"Game has finished - Player {board.player_turn} wins")  # Notify both terminals
                print(f"Final board:")
                print(board)
                sys.exit()

        # Use await for save_to_redis and publish
    else:
        print(f"\nIt is not your turn yet! Current player is {board.player_turn}.")
        print("\nCurrent board:")
        print(board)


async def listen_for_updates(redis_client, i_am_playing: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)
    
    print(f"Subscribed to {CHANNEL_NAME}, waiting for updates...")

    await handle_board_state(redis_client, i_am_playing)

    async for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"\nReceived update: {message['data']}")
            await handle_board_state(redis_client, i_am_playing)


async def main():
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe Game")
    
    parser.add_argument('--player', type=str, required=False, choices=['x', 'o'],
                        help="Choose 'x' or 'o' as the player symbol.")
    
    parser.add_argument('--reset', action='store_true',
                        help="Reset the game board and save to Redis.")

    args = parser.parse_args()

    if not args.player:
        print("Error: --player argument is required.")
        sys.exit(1) 

    r = redis.Redis(
        host="ai.thewcl.com",        
        port=6379,                   
        password="atmega328",
        db=12,         
        decode_responses=True        
    )

    if args.reset:
        board = tic_tac_toe_board.TicTacToeBoard()
        await board.reset(redis_client=r, path="game")
        print("Board has been reset!")
        return  

    board = await tic_tac_toe_board.TicTacToeBoard.load_from_redis(r, path="game")
    
    if not board:
        print("No saved game found, starting a new game!")
        board = tic_tac_toe_board.TicTacToeBoard()
        await board.save_to_redis(r, path="game") 
    
    board.player_turn = args.player  
    
    print(f"\nWelcome to Tic-Tac-Toe! You are playing as '{args.player}'\n")
    
    await listen_for_updates(r, args.player)

if __name__ == "__main__":
    asyncio.run(main())











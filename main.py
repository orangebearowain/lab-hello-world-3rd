from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
import redis.asyncio as redis
import tic_tac_toe_board

app = FastAPI()

r = redis.Redis(
    host="ai.thewcl.com",        
    port=6379,                   
    password="atmega328",
    db=12,         
    decode_responses=True        
    )


class MoveRequest(BaseModel):
    player: str
    index: int

class ResetRequest(BaseModel):
    reset: bool = True

async def load_board_from_redis():
    board = await tic_tac_toe_board.TicTacToeBoard.load_from_redis(r, path="game")
    return board

@app.get("/state")
async def get_game_state():
    board = await load_board_from_redis()
    if not board:
        raise HTTPException(status_code=404, detail="Game not found")
    return board.to_dict()

@app.post("/move")
async def make_move(request: MoveRequest):
    board = await load_board_from_redis()

    if not board:
        raise HTTPException(status_code=404, detail="Game not found")

    if board.state == "is finished":
        raise HTTPException(status_code=400, detail="Game has already ended")

    result = board.make_move(request.index)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    await board.save_to_redis(r, path="game")
    await r.publish("ttt_game_state_changed", "Board updated")

    return {"message": result["message"], "board": result.get("board", board.to_dict())}

@app.post("/reset")
async def reset_game(request: ResetRequest):
    board = tic_tac_toe_board.TicTacToeBoard()
    await board.reset(redis_client=r, path="game")

    return {"message": "Game has been reset.", "board": board.to_dict()}

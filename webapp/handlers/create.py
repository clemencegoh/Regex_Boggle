from ..DAO.gamestate import GameState
from .session import ID_TOKEN, TOKEN_SESSION
import json


def CreateNewGame(duration: int, random: bool, board: str):
    # create new gamestate
    g = GameState(duration, random, board)

    # cache in current session and set id
    current_id = g.GenerateNewID()
    token = g.GenerateToken()
    ID_TOKEN[current_id] = token
    TOKEN_SESSION[token] = g

    return json.dumps({
        'id': g.id,
        'token': g.token,
        'duration': g.duration,
        'board': g.gameboard.__str__()
    })





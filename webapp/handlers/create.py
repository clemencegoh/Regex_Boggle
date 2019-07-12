from ..DAO.gamestate import GameState
import json

# change to SQL if needed
ID_TOKEN = {}
TOKEN_SESSION = {}


def CreateNewGame(duration: int, random: bool, board: str):
    global ID_TOKEN, TOKEN_SESSION
    # create new gamestate
    g = GameState(duration, random, board)

    # cache in current session and set id
    id = g.GenerateNewID()
    token = g.GenerateToken()
    ID_TOKEN[id] = token
    TOKEN_SESSION[token] = g

    return json.dumps({
        'id': g.id,
        'token': g.token,
        'duration': g.duration,
        'board': g.gameboard.__str__()
    })





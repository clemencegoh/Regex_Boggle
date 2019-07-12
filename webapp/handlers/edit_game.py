from webapp.handlers.create import TOKEN_SESSION, ID_TOKEN
import json
import time


# todo: decide on scoring
# todo: complete this algorithm
def CheckWord(_word: str, gamestate: object):
    """
    Placeholder for now, will do the following:
    - Check if word is valid
    - Check if word is in dict
    - Add to points if both the above are true
    :param _word: word to check
    :param gamestate: current gamestate
    :return: None
    """
    pass


def EditGameState(_id: int, _token: str, _word: str) -> (bool, {}):
    if _id in ID_TOKEN:
        if _token == ID_TOKEN[_id]:
            g = TOKEN_SESSION[_token]
            time_left = g.endtime - time.time()
            if time_left <= 0:
                time_left = 0
                # del TOKEN_SESSION[ID_TOKEN[_id]]
                # del ID_TOKEN[_id]
            else:
                CheckWord(_word, g)

            return True, json.dumps({
                "id": g.id,
                "token": g.token,
                "duration": g.duration,
                "board": g.gameboard.__str__(),
                "time_left": time_left,
                "points": g.points
            })
    return False, ""



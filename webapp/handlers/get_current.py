from webapp.handlers.create import TOKEN_SESSION, ID_TOKEN
import json
import time


def GetCurrentState(_id: int) -> (bool, {}):
    if _id in ID_TOKEN:
        g = TOKEN_SESSION[ID_TOKEN[_id]]
        time_left = g.endtime - time.time()
        if time_left <= 0:
            time_left = 0

        resp = json.dumps({
            "id": g.id,
            "token": g.token,
            "duration": g.duration,
            "board": g.gameboard.__str__(),
            "time_left": time_left,
            "points": g.points
        })

        return True, resp
    else:
        return False, ""




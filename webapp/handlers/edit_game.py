from ..DAO.gamestate import GameState
from ..DAO.gameboard import GameBoard
from webapp.handlers.create import TOKEN_SESSION, ID_TOKEN
import json
import time


def Search(_word: str, gameboard: GameBoard) -> bool:
    """
    Search algorithm for word
    ! important to note that diagonals are ok too !

    :param _word: word to check
    :param gameboard: current gameboard
    :return: whether word is present
    """
    pass


def CheckWord(_word: str, gamestate: GameState, _valid_words: {str}) -> object:
    """
    Placeholder for now, will do the following:
    - Check if word is in dict
    - Check if word is valid
    - Add to points if both the above are true
    :param _word: word to check
    :param gamestate: current gamestate
    :param _valid_words: dict of valid words
    :return: new state
    """
    if _word in _valid_words:
        # word must be valid in the first place
        if Search(_word, gamestate.gameboard):
            # todo: add to score based on rules of boggle
            gamestate.points += 10

    return gamestate


def EditGameState(_id: int, _token: str,
                  _word: str, _valid_words: {}) -> (bool, {}):

    # validate id and token
    if _id in ID_TOKEN:
        if _token == ID_TOKEN[_id]:
            g = TOKEN_SESSION[_token]
            time_left = g.endtime - time.time()

            # check for time left, don't bother if over
            if time_left <= 0:
                time_left = 0
                # del TOKEN_SESSION[ID_TOKEN[_id]]
                # del ID_TOKEN[_id]
            else:
                g = CheckWord(_word, g, _valid_words)  # update state
                TOKEN_SESSION[_token] = g

            return True, json.dumps({
                "id": g.id,
                "token": g.token,
                "duration": g.duration,
                "board": g.gameboard.__str__(),
                "time_left": time_left,
                "points": g.points
            })
    return False, ""



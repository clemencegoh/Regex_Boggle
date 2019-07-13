from webapp.DAO.gamestate import GameState
from webapp.DAO.gameboard import GameBoard
from webapp.handlers.create import TOKEN_SESSION, ID_TOKEN
import json
import time

from webapp.data.valid_words import GetValidWords


def check_around_pos(i: int, j: int, word: str,
                     gameboard2D: [[str]],
                     seen: [[str]]) -> bool:
    # base case: exhausted path
    if len(word) == 0:
        return True

    # base case: limit exceeded
    if i < 0 or i >= len(gameboard2D) or j < 0 or j >= len(gameboard2D):
        return False

    # base case: seen before
    if seen[i][j]:
        return False

    # base case: current pos does not match
    if gameboard2D[i][j] != '*' and gameboard2D[i][j] != word[0]:
        return False

    # recursive
    seen[i][j] = True
    up = check_around_pos(i - 1, j, word[1:], gameboard2D, seen)
    up_right = check_around_pos(i-1, j+1, word[1:], gameboard2D, seen)
    right = check_around_pos(i, j + 1, word[1:], gameboard2D, seen)
    down_right = check_around_pos(i + 1, j + 1, word[1:], gameboard2D, seen)
    down = check_around_pos(i + 1, j, word[1:], gameboard2D, seen)
    down_left = check_around_pos(i - 1, j - 1, word[1:], gameboard2D, seen)
    left = check_around_pos(i, j - 1, word[1:], gameboard2D, seen)
    up_left = check_around_pos(i - 1, j - 1, word[1:], gameboard2D, seen)

    return up or up_right or right or down_right or down or down_left or left or up_left


def Search(_word: str, gameboard: GameBoard) -> bool:
    """
    Search algorithm for word
    ! important to note that diagonals are ok too !

    :param _word: word to check
    :param gameboard: current gameboard
    :return: whether word is present
    """
    found = False
    pos = []

    try:
        pos = gameboard.positions[_word[0]]  # get starting positions
        pos.extend(gameboard.positions['*'])  # every * is a possible start too
    except KeyError:
        pass

    for coords in pos:
        seen = [[False for i in range(4)] for j in range(4)]
        found = found or check_around_pos(coords[0],
                                           coords[1],
                                           _word,
                                           gameboard.gameboard2D,
                                           seen)
        # optimisation
        if found:
            return True
    return False


def CheckWord(_word: str, gamestate: GameState, _valid_words: {str}) -> GameState:
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
    # check if tried already
    if _word not in gamestate.tried_words:
        gamestate.tried_words.add(_word)

        # check if valid word
        if _word in _valid_words:

            # check if in gameboard
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


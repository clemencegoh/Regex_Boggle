import time
import hashlib
import json
import webapp.DAO.gameboard as g


GLOBAL_COUNTER = 0


def getNewID():
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1
    return GLOBAL_COUNTER


class GameState:
    def __init__(self, _duration,
                 _random=False,
                 _board="",
                 _id=0,
                 _token=""):

        self.duration = _duration
        self.endtime = time.time() + _duration
        self.id = _id
        self.gameboard = g.GameBoard()
        self.token = _token
        self.points = 0
        self.tried_words = set()

        if not _random:
            if not _board:
                self.gameboard.UseDefaultBoard('webapp/data/test_board.txt')
            else:
                self.gameboard.from_gameboard_string(_board)
        else:
            self.gameboard.CreateNewBoard()
        self.gameboard.init_positions()

    def GenerateNewID(self):
        """
        ! IMPORTANT !
        This must only be called once
        :return: new ID
        """
        self.id = getNewID()
        return self.id

    def GenerateToken(self):
        """
        Generates unique token using hash
        :return:
        """
        message = str(self.endtime) + str(self.id) + str(self.gameboard)
        self.token = hashlib.sha256(message.encode()).hexdigest()
        return self.token






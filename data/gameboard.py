"""
Helper functions for reading and creating data files
"""

import string
import random

ALL_POSSIBLE = list(string.ascii_uppercase + '*')


class GameBoard:
    """
    Gameboard should be the object that
    determines the current state of the game
    """
    def __init__(self, existing_board:[[str]] = None):
        self.gameboard = ""
        self.gameboard2D = [[''] * 4] * 4  # initialise with fixed size

        if existing_board:
            self.gameboard2D = existing_board
            for pos, row in enumerate(existing_board):
                self.gameboard += ', '.join(row)
                if pos != len(existing_board)-1:
                    self.gameboard += ', '

    def CreateNewBoard(self):
        """
        Creates new board as comma-separated string
        """
        # init new if not already empty
        self.gameboard = ""
        self.gameboard2D = [[''] * 4] * 4

        for i in range(4):
            for j in range(4):
                chosen = random.choice(ALL_POSSIBLE)
                if i == 3 and j == 3:
                    self.gameboard += chosen
                else:
                    self.gameboard += "{}, ".format(chosen)
                self.gameboard2D[i][j] = chosen

    def UseDefaultBoard(self):
        # todo: might have to change this to accept filepath string later
        """
        Uses default board from test_board
        :return: default board as string
        """
        with open('test_board.txt', 'r') as f:
            self.gameboard = f.read().strip()
            parsed_gameboard = self.gameboard.split(', ')
            for i in range(4):
                for j in range(4):
                    self.gameboard2D[i][j] = parsed_gameboard[i+j]

    def __str__(self):
        """
        Override string method so it gives the gameboard when called
        :return: gameboard as string
        """
        return self.gameboard







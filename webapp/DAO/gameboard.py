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
    def __init__(self):
        self.gameboard = ""
        self.gameboard2D = []
        self.positions = {}  # positions to help with algorithm

    def init_positions(self):
        if len(self.positions) <= 1:  # prevents from double init
            for i in range(len(self.gameboard2D)):
                for j in range(len(self.gameboard2D[0])):
                    if self.gameboard2D[i][j] not in self.positions:
                        self.positions[self.gameboard2D[i][j]] = [(i, j)]
                    else:
                        self.positions[self.gameboard2D[i][j]].append((i, j))

    def from_gameboard_string(self, board):
        self.gameboard = board
        parsed_gameboard = self.gameboard.split(', ')
        if len(parsed_gameboard) != 16:
            # use default
            self.UseDefaultBoard('webapp/data/test_board.txt')
            return
        parsed_gameboard = [x.upper() for x in parsed_gameboard]
        self.gameboard2D = []
        counter = 0

        for i in range(4):
            self.gameboard2D.append([])
            for j in range(4):
                self.gameboard2D[i].append(parsed_gameboard[counter])
                counter += 1

    def from_2D_array(self, existing_board):
        self.gameboard2D = existing_board
        for pos, row in enumerate(existing_board):
            self.gameboard += ', '.join(row)
            if pos != len(existing_board) - 1:
                self.gameboard += ', '

    # public functions
    def CreateNewBoard(self):
        """
        Creates new board as comma-separated string
        """
        # init new if not already empty
        self.gameboard = ""
        self.gameboard2D = []

        for i in range(4):
            self.gameboard2D.append([])
            for j in range(4):
                chosen = random.choice(ALL_POSSIBLE)
                if i == 3 and j == 3:
                    self.gameboard += chosen
                else:
                    self.gameboard += "{}, ".format(chosen)
                self.gameboard2D[i].append(chosen)

    def UseDefaultBoard(self, filepath):
        """
        Uses default board from test_board
        :return: default board as string
        """
        with open(filepath, 'r') as f:
            self.from_gameboard_string(f.read().strip())

    def __str__(self):
        """
        Override string method so it gives the gameboard when called
        :return: gameboard as string
        """
        return self.gameboard







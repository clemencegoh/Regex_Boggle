"""
Tests for all endpoints
"""

import unittest
import webapp.DAO.gameboard as gameboard


class TestDataParser(unittest.TestCase):

    def setUp(self) -> None:
        self.Gameboard = gameboard.GameBoard()

    def test_create_board(self):
        """
        functional test for parsing of data
        :return:
        """
        self.Gameboard.CreateNewBoard()
        new_board = self.Gameboard.gameboard
        self.assertEqual(len(new_board.split(", ")), 16,
                         "Length of board created not 16\nBoard: {}".format(new_board))
        if new_board[0] != '*':
            self.assertTrue(new_board[0].isupper(), "Not uppercase letter, got {}".format(new_board[0]))

    def test_use_existing(self):
        self.Gameboard.UseDefaultBoard('../data/test_board.txt')
        self.assertEqual('T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D',
                         self.Gameboard.gameboard,
                         "Gameboard was parsed wrongly")


if __name__ == '__main__':
    unittest.main()

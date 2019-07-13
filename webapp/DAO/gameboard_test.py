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

        self.assertNotEqual(self.Gameboard.gameboard2D[0],
                            self.Gameboard.gameboard2D[1],
                            "Should not be the same, odds are low")

        self.assertEqual(len(new_board.split(", ")), 16,
                         "Length of board created not 16\nBoard: {}".format(new_board))
        if new_board[0] != '*':
            self.assertTrue(new_board[0].isupper(), "Not uppercase letter, got {}".format(new_board[0]))

    def test_use_existing(self):
        self.Gameboard.UseDefaultBoard('../data/test_board.txt')
        self.assertEqual('T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D',
                         self.Gameboard.gameboard,
                         "Gameboard was parsed wrongly")

    def test_parse_positions(self):
        self.Gameboard.UseDefaultBoard('../data/test_board.txt')
        self.Gameboard.init_positions()
        self.assertEqual({
            'T': [(0, 0)],
            'A': [(0, 1), (1, 1)],
            'P': [(0, 2)],
            '*': [(0, 3), (3, 1)],
            'E': [(1, 0)],
            'K': [(1, 2)],
            'S': [(1, 3), (2, 3), (3, 0)],
            'O': [(2, 0)],
            'B': [(2, 1)],
            'R': [(2, 2)],
            'X': [(3, 2)],
            'D': [(3, 3)]
        }, self.Gameboard.positions)


if __name__ == '__main__':
    unittest.main()

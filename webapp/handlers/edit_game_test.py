"""
Tests for all endpoints
"""

import unittest
from webapp.handlers.edit_game import CheckWord, Search
from webapp.DAO.gamestate import GameState
from webapp.data.valid_words import GetValidWords


class TestEndpoints(unittest.TestCase):

    def setUp(self) -> None:
        self.GameState = GameState(1000)
        self.GameState.GenerateNewID()
        self.GameState.GenerateToken()
        self.assertIsNotNone(self.GameState.gameboard.gameboard2D)
        self.valid = GetValidWords('../data/dictionary.txt')

    def test_search_valid(self):
        pass

    def test_search_invalid(self):
        pass

    def test_checkword_valid(self):
        words = ['TAPES']
        is_zero = [False]
        points = []
        for w in words:
            new_state = CheckWord(w, self.GameState, self.valid)
            self.assertIsNotNone(new_state)
            points.append(new_state.points)
        for pos, zero in enumerate(is_zero):
            if not zero:
                self.assertNotEqual(0, points[pos])
            else:
                self.assertEqual(0, points[pos])

    def test_checkword_invalid(self):
        pass

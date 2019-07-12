"""
Tests for all endpoints
"""

import unittest
import webapp.DAO.gamestate as gamestate


class TestDataParser(unittest.TestCase):

    def setUp(self) -> None:
        self.GameState = gamestate.GameState(1000)

    def test_id_creation(self):
        """
        functional test for parsing of data
        :return:
        """
        current_id = self.GameState.GenerateNewID()
        self.assertIsNotNone(current_id, "Should not be none at all, {}".format(current_id))
        next_id = self.GameState.GenerateNewID()
        self.assertNotEqual(current_id, next_id, "Global_counter not working as intended")

    def test_token_generation(self):
        current_id = self.GameState.GenerateNewID()
        current_token = self.GameState.GenerateToken()
        next_token = self.GameState.GenerateToken()
        self.assertEqual(current_token, next_token,
                         "Token generation should be unique.")
        self.assertEqual(current_id, self.GameState.id,
                         "gamestate id not equal, likely fail if above fails.")


if __name__ == '__main__':
    unittest.main()

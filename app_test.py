"""
Tests for all endpoints
"""

import unittest
import requests
import json


BASE_URL = 'http://localhost:5000/games'


class TestEndpoints(unittest.TestCase):

    def test_create_valid(self):
        """
        Create new game with valid params
        :return: 201 response with json
        """
        params = {
            "duration": 1000,
            "random": True,
            "board": ""
        }
        resp = requests.post(BASE_URL, params=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")
        content = json.loads(resp.content)
        print(content)
        self.assertIsNotNone(content, "No json body returned")
        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))

    def test_create_invalid(self):
        """
        Create new game with invalid params
        - Duration
        - Random + board
        :return: should not give 201
        """
        pass

    def test_play_valid(self):
        """
        test play with valid token
        :return: 200
        """
        pass

    def test_play_invalid(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 400
        """
        pass

    def test_get_status_valid(self):
        """
        valid test for getting current status of the game
        - id
        :return: 200
        """
        pass

    def test_get_status_invalid(self):
        """
        valid test for getting current status of the game
        - missing id
        :return: 400
        """
        pass


if __name__ == '__main__':
    unittest.main()

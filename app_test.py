"""
Tests for all endpoints
"""

import unittest
import requests
import json
import time


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
        resp = requests.post(BASE_URL, data=params)
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
        params = {
            "duration": 1000,
            "board": ""
        }
        resp = requests.post(BASE_URL, data=params)
        self.assertEqual(resp.status_code, 400, "response code not correct")

    def test_play_valid(self):
        """
        test play with valid token
        :return: 200
        """
        params = {
            "duration": 1000,
            "random": False,
            "board": ""
        }
        resp = requests.post(BASE_URL, data=params)
        self.assertEqual(resp.status_code, 201, resp.content)
        content = json.loads(resp.content)
        gid = content['id']
        token = content['token']
        duration = content['duration']
        board = content['board']

        params = {
            'id': gid,
            'token': token,
            'word': 'TAPE'
        }
        resp = requests.put(BASE_URL + '/' + str(gid), data=params)
        self.assertEqual(resp.status_code, 200, resp)
        content = json.loads(resp.content)

        print(content)

        # ensure response correct
        self.assertIsNotNone(content, "No json body returned")

        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertEqual(content['id'], gid, 'id does not match')

        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertEqual(content['token'], token, 'token does not match')

        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertEqual(content['duration'], duration, 'duration does not match')

        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))
        self.assertEqual(content['board'], board)

        self.assertLess(content['time_left'], duration, 'time left should not be greater than duration')

        self.assertEqual(4, content['points'])

    def test_play_invalid_id(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 400
        """
        params = {
            "duration": 1000,
            "random": False,
            "board": ""
        }
        resp = requests.post(BASE_URL, data=params)
        self.assertEqual(resp.status_code, 201, resp.content)
        content = json.loads(resp.content)
        gid = content['id']
        token = content['token']

        params = {
            'id': 1000,
            'token': token,
            'word': 'TAPE'
        }
        resp = requests.put(BASE_URL + '/1000', data=params)
        self.assertEqual(resp.status_code, 400, resp)

    def test_play_invalid_token(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 400
        """
        params = {
            "duration": 1000,
            "random": False,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, resp.content)
        content = json.loads(resp.content)
        gid = content['id']
        token = content['token']

        params = {
            'id': gid,
            'token': "00000",
            'word': 'TAPE'
        }
        resp = requests.put(BASE_URL + '/' + str(gid), json=params)
        self.assertEqual(resp.status_code, 400, resp)

    def test_get_status_valid(self):
        """
        valid test for getting current status of the game
        - id
        :return: 200
        """
        params = {
            "duration": 1000,
            "random": True,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        content = json.loads(resp.content)
        gid = content['id']
        token = content['token']
        duration = content['duration']
        board = content['board']

        time.sleep(2)

        resp = requests.get(BASE_URL + "/" + str(gid))
        self.assertEqual(200, resp.status_code, "response code not correct")
        content = json.loads(resp.content)
        print(content)
        self.assertIsNotNone(content, "No json body returned")

        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertEqual(content['id'], gid, 'id does not match')

        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertEqual(content['token'], token, 'token does not match')

        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertEqual(content['duration'], duration, 'duration does not match')

        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))
        self.assertEqual(content['board'], board)

        self.assertLess(content['time_left'], duration, 'time left should not be greater than duration')

        self.assertEqual(content['points'], 0)

    def test_get_status_invalid(self):
        """
        valid test for getting current status of the game
        - missing id
        :return: 400
        """
        resp = requests.get(BASE_URL + "/" + "100")
        self.assertEqual(400, resp.status_code, "response code not correct")


if __name__ == '__main__':
    unittest.main()

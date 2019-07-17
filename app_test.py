"""
Tests for all endpoints
"""

import unittest
import requests
import json
import time


BASE_URL = 'http://18.236.132.102/games'


class TestCreateEndpoint(unittest.TestCase):

    def test_create_valid_random(self):
        """
        Create new game with valid params
        :return: 201 response with json
        """
        params = {
            "duration": 1000,
            "random": True,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
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
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 400, "response code not correct")

    def test_create_valid_non_random(self):
        params = {
            "duration": 1000,
            "random": False,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")
        content = json.loads(resp.content)
        print(content)
        self.assertIsNotNone(content, "No json body returned")

        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))

        # Should default to hardcoded
        self.assertEqual(content['board'], 'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D')

    def test_create_valid_random_board(self):
        params = {
            "duration": 1000,
            "random": True,
            "board": 'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D',
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")
        content = json.loads(resp.content)
        print(content)
        self.assertIsNotNone(content, "No json body returned")

        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))

        # Should NOT be same as hardcoded
        self.assertNotEqual(content['board'], 'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D')

    def test_create_valid_wrong_random_type(self):
        """
        Create new game with invalid type for random
        - Duration
        - Random + board
        :return: should not give 201
        """
        params = {
            "duration": 1000,
            'random': "true",
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")

    def test_create_invalid_type_duration(self):
        """
        Create new game with invalid type for duration
        - Duration
        - Random + board
        :return: should not give 201
        """
        params = {
            "duration": '1000',
            'random': True,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")

    def test_create_false_invalid_board(self):
        params = {
            "duration": 1000,
            "random": False,
            "board": 'T, X, D',
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, "response code not correct")
        content = json.loads(resp.content)
        print(content)
        self.assertIsNotNone(content, "No json body returned")

        self.assertTrue(content['id'], 'id empty: {}'.format(content['id']))
        self.assertTrue(content['token'], 'token empty: {}'.format(content['token']))
        self.assertTrue(content['duration'], 'duration empty: {}'.format(content['duration']))
        self.assertTrue(content['board'], 'board empty: {}'.format(content['board']))

        # Should be same as hardcoded
        self.assertEqual(content['board'], 'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D')


####
# Create
####


class TestPlayEndpoint(unittest.TestCase):
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
        resp = requests.post(BASE_URL, json=params)
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
        resp = requests.put(BASE_URL + '/' + str(gid), json=params)
        self.assertEqual(resp.status_code, 200, resp.content)
        content = json.loads(resp.content)

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
        :return: 404
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
            'id': 1000,
            'token': token,
            'word': 'TAPE'
        }
        resp = requests.put(BASE_URL + '/hii', json=params)
        self.assertEqual(resp.status_code, 404, resp)

    def test_play_invalid_token(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
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
        self.assertEqual(resp.status_code, 404, resp)

    def test_play_missing_word(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
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
            'token': token,
        }
        resp = requests.put(BASE_URL + '/' + str(gid), json=params)
        self.assertEqual(resp.status_code, 404, resp)

    def test_play_wrong_type_duration(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
        """
        params = {
            "duration": 'absc',
            "random": False,
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 400, resp.content)

    def test_play_wrong_type_random(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
        """
        params = {
            "duration": 1000,
            "random": 'false',
            "board": ""
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, resp.content)

    def test_play_wrong_type_board(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
        """
        params = {
            "duration": 1000,
            "random": False,
            "board": 10,
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, resp.content)

    def test_play_mismatch_id(self):
        """
        test play with invalid token
        - missing id
        - missing token
        - missing word
        :return: 404
        """
        params = {
            "duration": 1000,
            "random": False,
            "board": "",
        }
        resp = requests.post(BASE_URL, json=params)
        self.assertEqual(resp.status_code, 201, resp.content)
        content = json.loads(resp.content)
        gid = content['id']
        token = content['token']

        params = {
            'token': token,
            'word': 'TAPE'
        }
        resp = requests.put(BASE_URL + '/' + str(gid + 100), json=params)
        self.assertEqual(resp.status_code, 404, resp)


######
# GET endpoint
######


class TestGetEndpoint(unittest.TestCase):
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
        self.assertEqual(404, resp.status_code, "response code not correct")

    def test_get_status_invalid_negative(self):
        """
        valid test for getting current status of the game
        - negative int id
        :return: 404
        """
        resp = requests.get(BASE_URL + "/" + "-1")
        self.assertEqual(404, resp.status_code, "response code not correct")

    def test_get_status_invalid_string(self):
        """
        valid test for getting current status of the game
        - string id
        :return: 400
        """
        resp = requests.get(BASE_URL + "/" + "hello")
        self.assertEqual(404, resp.status_code, "response code not correct")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCreateEndpoint())

    play_suite = unittest.TestSuite()
    play_suite.addTest(TestPlayEndpoint())

    get_suite = unittest.TestSuite()
    get_suite.addTest(TestGetEndpoint())

    unittest.TestRunner().run(suite)
    # unittest.TestRunner().run(play_suite)
    # unittest.TestRunner().run(get_suite)

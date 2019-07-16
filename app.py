"""
Endpoints needed:
- Create Game: /games -> POST, returns 201 with json
- Play existing game: /games/:id -> PUT, returns 200 with json
- Show existing game: /games/:id -> GET, returns 200 with json
"""

from flask import Flask, request
from webapp.handlers.create import CreateNewGame
from webapp.handlers.get_current import GetCurrentState
from webapp.handlers.edit_game import EditGameState
from webapp.data.valid_words import GetValidWords
import argparse
import json


# Variables here
app = Flask(__name__)
SAVE_DIR = './saved_states/'

# Init upon start, do only once
VALID_WORDS = GetValidWords('webapp/data/dictionary.txt')


def bad_response(msg: str):
    response = app.response_class(
        response=msg,
        status=400
    )
    return response


def custom_bool_conversion(arg: str):
    positives = {'true', 'True', 'yes', 'YES', 'Yes', 'y', 'Y', True}
    # negatives = {'false', 'False', 'no', 'NO', 'No', 'n', 'N'}
    if arg in positives:
        return True
    return False


@app.route('/', methods=['GET'])
def home():
    return "Welcome!"


@app.route('/games', methods=['POST'])
def create_game():
    """
    Parameters:
        - Duration (time in seconds)
        - Random (bool, whether to initiate new board)
        - Board (if not random, will use this)
    :return: 201
    """

    content = json.loads(request.data.decode())
    print(content)

    try:
        duration = content["duration"]
        random = content['random']

        if not duration:
            # required fields
            return bad_response("duration unfilled")

        random = custom_bool_conversion(random)  # catches string variables for random
        duration = int(duration)

        try:
            board = content['board']
        except KeyError:
            board = ""

        # create new game here and save
        data = CreateNewGame(duration, random, board)
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response

    except KeyError:
        return json.dumps({"message": "Invalid parameters"}), 400

    except Exception as e:
        return json.dumps({"message": e}), 400


@app.route('/games/<gid>', methods=['PUT', 'GET'])
def edit_game(gid):

    if request.method == "GET":
        # Get current status of game
        present, status = GetCurrentState(int(gid))
        if not present:
            return json.dumps({"message": "No such game session"}), 404
        return status
    else:
        content = json.loads(request.data.decode())

        # make a change to the game state
        token = content['token']
        word = content['word'].upper()
        try:
            present, status = EditGameState(int(gid), token, word, VALID_WORDS)
            if not present:
                return json.dumps({"message": "Wrong Word or invalid params"}), 404

            return status
        except Exception as e:
            print(e)
            return json.dumps({"message": "Game not found"}), 404

app.run(port=5000)


# if __name__ == "__main__":
#     """
#     For development purposes only,
#     single-threaded instance
#     """
#
#     parser = argparse.ArgumentParser(description='Runs server for boggle webapp')
#     parser.add_argument('--dev', action='store_true',
#                         help='run in dev mode on port 5000')
#
#     args = parser.parse_args()
#
#     print(args.dev)
#
#     if args.dev:
#         app.run(port=5000)
#     else:
#         app.run(host="0.0.0.0", port=80)

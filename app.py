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


def create_response(msg: str, code: int):
    return json.dumps({
        "message": msg,
    }), code


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
    content = json.loads(request.data)

    try:
        duration = content["duration"]
        random = content['random']

        if not duration or type(duration) != int:
            # required fields
            return create_response("duration error", 400)
        if type(random) != bool:
            return create_response("random type incorrect", 400)

        # random = custom_bool_conversion(random)  # catches string variables for random
        # duration = int(duration)

        if duration < 0:
            return create_response("duration must be greater than 0", 400)
        try:
            board = content['board']
            if type(board) != str:
                return create_response("board type incorrect", 400)
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
        return json.dumps({"message": "Invalid or missing parameters"}), 400

    except Exception as e:
        return json.dumps({"message": e}), 400


@app.route('/games/<gid>', methods=['PUT', 'GET'])
def edit_game(gid):

    if request.method == "GET":
        # Get current status of game

        try:
            gid = int(gid)
        except ValueError:
            return create_response("Invalid id type", 400)

        present, status = GetCurrentState(gid)
        if not present:
            return create_response("No such game session", 404)
        return status
    else:
        content = json.loads(request.data)

        # make a change to the game state
        try:
            gid_data = content['id']
            token = content['token']
            word = content['word']

            if type(token) != str or type(word) != str or type(gid_data) != int:
                return create_response("invalid type for token or word", 400)

            try:
                gid = int(gid)
                gid_data = int(gid_data)
            except ValueError:
                return create_response("Invalid id type", 400)

            if gid != gid_data:
                return create_response("id does not match", 400)

            word = word.upper()

            present, status = EditGameState(int(gid), token, word, VALID_WORDS)
            if not present:
                return create_response("Wrong word or invalid", 404)

            return status
        except KeyError:
            return create_response("missing parameters", 400)
        except Exception as e:
            print(e)
            return create_response(e.__str__(), 404)

# app.run(port=5000)


if __name__ == "__main__":
    """
    For development purposes only,
    single-threaded instance
    """

    parser = argparse.ArgumentParser(description='Runs server for boggle webapp')
    parser.add_argument('--dev', action='store_true',
                        help='run in dev mode on port 5000')

    args = parser.parse_args()

    print(args.dev)

    if args.dev:
        app.run(port=5000)
    else:
        app.run(host="0.0.0.0", port=80)

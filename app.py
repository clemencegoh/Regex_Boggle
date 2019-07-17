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


def custom_bool_conversion(arg) -> bool:
    positives = {'true', 'True', 'yes', 'YES', 'Yes', 'y', 'Y', True, 1}
    # negatives = {'false', 'False', 'no', 'NO', 'No', 'n', 'N'}
    if arg in positives:
        return True
    return False


def custom_duration_conversion(arg) -> int:
    try:
        arg = int(arg)
        return arg
    except ValueError:
        return -1


def custom_board_conversion(content) -> str:
    try:
        board = content['board']
        if type(board) != str:
            return ""  # accept it anyway
        return board
    except KeyError:
        return ""


def custom_gid_conversion(arg) -> int:
    try:
        gid = int(arg)
        return gid
    except ValueError:
        return -1


def custom_token_conversion(content) -> str:
    try:
        token = content['token']
        token = str(token)
        return token
    except KeyError:
        return "Error"


def custom_word_conversion(content) -> str:
    try:
        word = content['word']
        word = str(word).upper()
        return word
    except KeyError:
        return "!Error!"


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

        # convert duration to int
        duration = custom_duration_conversion(duration)

        # convert random to bool
        random = custom_bool_conversion(random)

        board = custom_board_conversion(content)

        if duration < 0:
            return create_response("duration param error", 400)
        if board == "Error":
            return create_response("board error", 400)

        # create new game here and save
        data = CreateNewGame(duration, random, board)
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response

    except KeyError:
        return create_response("one or more params invalid or missing", 400)


@app.route('/games/<gid>', methods=['PUT', 'GET'])
def edit_game(gid):

    if request.method == "GET":
        # Get current status of game

        gid = custom_gid_conversion(gid)

        if gid == -1:
            return create_response("invalid id", 404)

        present, status = GetCurrentState(gid)
        if not present:
            return create_response("No such game session", 404)
        return status
    else:
        content = json.loads(request.data)

        # make a change to the game state
        try:
            token = custom_token_conversion(content)
            word = custom_word_conversion(content)
            gid = custom_gid_conversion(gid)

            if token == "Error" or word == "!Error!" or gid == -1:
                return create_response("Invalid token or word or id", 404)

            present, status = EditGameState(gid, token, word, VALID_WORDS)
            if not present:
                return create_response("Wrong word or invalid", 404)

            return status
        except KeyError:
            return create_response("missing or invalid parameters", 400)
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

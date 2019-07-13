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
    positives = {'true', 'True', 'yes', 'YES', 'Yes', 'y', 'Y'}
    # negatives = {'false', 'False', 'no', 'NO', 'No', 'n', 'N'}
    if arg in positives:
        return True
    return False


@app.route('/games', methods=['POST'])
def create_game():
    """
    Parameters:
        - Duration (time in seconds)
        - Random (bool, whether to initiate new board)
        - Board (if not random, will use this)
    :return: 201
    """

    duration = request.args.get("duration")
    random = request.args.get('random')

    if not duration or not random:
        # required fields
        return bad_response("one or more fields unfilled")

    try:
        random = custom_bool_conversion(random)
        duration = int(duration)
        board = request.args.get('board')

        # create new game here and save
        data = CreateNewGame(duration, random, board)
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response
    except ValueError:
        return bad_response("unable to parse duration")
    except Exception as e:
        return bad_response("{}".format(e))


@app.route('/games/<gid>', methods=['PUT', 'GET'])
def edit_game(gid):
    if request.method == "GET":
        # Get current status of game
        present, status = GetCurrentState(int(gid))
        if not present:
            return bad_response("No such id present")
        return status
    else:
        # make a change to the game state
        token = request.args.get('token')
        word = request.args.get('word')
        present, status = EditGameState(int(gid), token, word, VALID_WORDS)
        if not present:
            return bad_response("Wrong ID or token")

        return status


if __name__ == "__main__":
    """
    For development purposes only,
    single-threaded instance
    """
    # app.run(host="0.0.0.0", port=80)
    app.run(port=5000)

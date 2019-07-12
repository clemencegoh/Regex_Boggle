"""
Endpoints needed:
- Create Game: /games -> POST, returns 201 with json
- Play existing game: /games/:id -> PUT, returns 200 with json
- Show existing game: /games/:id -> GET, returns 200 with json
"""

from flask import Flask, request
from webapp.handlers.create import CreateNewGame


# Variables here
app = Flask(__name__)
SAVE_DIR = './saved_states/'


@app.route('/games', methods=['POST'])
def create_game():
    """
    Parameters:
        - Duration (time in seconds)
        - Random (bool, whether to initiate new board)
        - Board (if not random, will use this)
    :return: 201
    """

    duration = request.form.get("duration")
    random = request.form.get("random")

    if not duration or not random:
        # check again
        duration = request.args.get("duration")
        random = request.args.get('random')

        if not duration or not random:
            # required fields
            response = app.response_class(
                response="one or more fields unfilled",
                status=400
            )
            return response

    try:
        random = bool(random)
        duration = int(duration)
        board = request.form.get("board")
        if not board:
            board = request.args.get('board')
        data = CreateNewGame(duration, random, board)
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response
    except ValueError:
        response = app.response_class(
            response="unable to parse duration",
            status=400
        )
        return response
    except Exception:
        print('here?')
        response = app.response_class(
            response="unable to parse random",
            status=400
        )
        return response


@app.route('/games/<id>', methods=['PUT', 'GET'])
def edit_game(id):
    if request.method == "GET":
        # Get current status of game
        pass
    else:
        # make a change to the game state
        pass


if __name__ == "__main__":
    """
    For development purposes only,
    single-threaded instance
    """
    # app.run(host="0.0.0.0", port=80)
    app.run(port=5000)

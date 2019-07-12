"""
Endpoints needed:
- Create Game: /games -> POST, returns 201 with json
- Play existing game: /games/:id -> PUT, returns 200 with json
- Show existing game: /games/:id -> GET, returns 200 with json
"""

from flask import Flask, request


# Variables here
app = Flask(__name__)
SAVE_DIR = './saved_states/'


@app.route('/games', methods=['POST'])
def create_game():
    return 'Hello, World!'


@app.route('/games/<id>', methods=['PUT', 'GET'])
def edit_game(id):
    if request.method == "GET":
        # Get current status of game
        pass
    else:
        # make a change to the game state
        pass


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80)
    app.run(port=8080)
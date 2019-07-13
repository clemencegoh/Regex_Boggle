# Regex_Boggle
Web api implementing the boggle game with a regex addition allowing '*' as a character.


## Solution
- 3 endpoints:
    1. /games
        - POST
    2. /games/:id
        - GET
        - PUT
        
## Rules
- Rules of boggle game:
    1. To start, POST to /games to get id and token
        - **duration field required**
        - **random field required**
    2. To get current state of game and current points, GET to /games/:id
    3. To start guessing a word, PUT to /games/:id
        - Every word guessed will add 10 points
        - Once time is up, points will no longer be updated.
- Objective: 
    - To get as many points as possible within the set duration
        
## What it does
1. Creates a new game.
    - Params:
        - ```
            duration (required): int,
            random (required): bool,
            board : str
          ```
    - Response:
        - ```
            201, 
            {
              "id": 1,
              "token": "9dda26ec7e476fb337cb158e7d31ac6c",
              "duration": 12345,
              "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"
            }
          ```
2. Edit current game
    - Params:
        - ```
            id (required): int,
            token (required): str,
            word (required) : str
          ```
    - Response:
        - ```
            200, 
            {
              "id": 1,
              "token": "9dda26ec7e476fb337cb158e7d31ac6c",
              "duration": 12345,
              "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K",
              "time_left": 10000,
              "points": 10
            }
          ```
    - How it's implemented:
        - Uses a dictionary to store game states currently in play
            - Transferring this into a json format and putting it into 
            a file or database reduces memory but increases query time.
        - Every time a query for a word is made, saves the query and
        checks if it is a valid word and if the word is present within
        the boggle.
        
          
3. Edit current game
    - Params:
        - ```
            id (required): int
          ```
    - Response:
        - ```
            200, 
            {
              "id": 1,
              "token": "9dda26ec7e476fb337cb158e7d31ac6c",
              "duration": 12345,
              "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K",
              "time_left": 10000,
              "points": 10
            }
          ```


## How to setup
1. Git clone the repo
2. install python3
3. use command `pip install -r requirements.txt`
    - This installs flask and any other packages required
4. `python3 app.py --dev` for running on localhost:5000
    - Alternatively, run `python3 app.py` for port 80
5. Run Integrated tests using tests in `app_test.py`
    - Or run unit tests in their respective folders
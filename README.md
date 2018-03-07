# Readme #

This is a REST API to play Mastermind game.

# Requirements #

- Python 3.6
- virtualenv
- git

# Install instructions #

1. Clone this repository:

        $ git clone https://github.com/oriolgg/mastermind

2. Create and source a virtualenv for this project:

        $ virtualenv mastermind_env ; source mastermind_env/bin/activate

3. Install dependenciesfor this project:

        $ cd mastermind ; pip install -r requirements.txt

4. Generate the Database to save the games:

        $ python manage.py migrate

5. Run the server:

        $ python manage.py runserver

# How it works #

- Start a new Mastermind game:

    Execute a POST request to the endpoint http://localhost:8000/mastermind/game

    This will create a game with 4 pegs and 5 possible choices per peg and return its json representation:

        {
            "res": "OK",
            "error": "",
            "data": {
                "id": 1,
                "started_at": "2018-03-07 11:23:52",
                "state": "NEW",
                "num_pegs": 6,
                "num_choices": 6,
                "num_attempts": 0,
                "attempts": []
            }
        }

    You can change the number of pegs or possible choices to make the game easier or harder by passing the variables "numberOfPegs" and "numberOfChoices".

    It will not show the pattern created.

- Get current state of some game:

    Execute a GET request to the endpoint http://localhost:8000/mastermind/game/{id}

    This will return a json representation of this game, including all the attempts that the user has made:

        {
            "res": "OK",
            "error": "",
            "data": {
                "id": 1,
                "started_at": "2018-03-07 11:23:52",
                "state": "COMPLETED",
                "num_pegs": 6,
                "num_choices": 6,
                "num_attempts": 8,
                "attempts": [
                    {
                        "id": 1,
                        "attempted_at": "2018-03-07 12:06:26",
                        "guess": "RED,RED,RED,RED,RED,RED",
                        "black": 0,
                        "white": 0
                    },
                    {
                        "id": 2,
                        "attempted_at": "2018-03-07 12:07:02",
                        "guess": "RED,RED,RED,RED,RED,WHITE",
                        "black": 0,
                        "white": 0
                    },
                    {
                        "id": 3,
                        "attempted_at": "2018-03-07 12:07:27",
                        "guess": "RED,RED,RED,RED,RED,YELLOW",
                        "black": 1,
                        "white": 0
                    },
                    {
                        "id": 4,
                        "attempted_at": "2018-03-07 12:07:48",
                        "guess": "YELLOW,RED,RED,RED,YELLOW,YELLOW",
                        "black": 3,
                        "white": 0
                    },
                    {
                        "id": 5,
                        "attempted_at": "2018-03-07 12:07:58",
                        "guess": "RED,YELLOW,RED,RED,YELLOW,YELLOW",
                        "black": 2,
                        "white": 1
                    },
                    {
                        "id": 6,
                        "attempted_at": "2018-03-07 12:09:11",
                        "guess": "YELLOW,MAROON,RED,MAROON,YELLOW,YELLOW",
                        "black": 5,
                        "white": 0
                    },
                    {
                        "id": 7,
                        "attempted_at": "2018-03-07 12:09:18",
                        "guess": "YELLOW,MAROON,MAROON,RED,YELLOW,YELLOW",
                        "black": 4,
                        "white": 1
                    },
                    {
                        "id": 8,
                        "attempted_at": "2018-03-07 12:09:36",
                        "guess": "YELLOW,MAROON,GRAY,MAROON,YELLOW,YELLOW",
                        "black": 6,
                        "white": 0
                    }
                ],
                "pattern": "YELLOW,MAROON,GRAY,MAROON,YELLOW,YELLOW"
            }
        }

    It will not show the pattern created unless the user guesses it.

- Guess a solution of some game:

    Execute a POST request to the endpoint http://localhost:8000/mastermind/game/{id}/guess with one variable in the body "guess":

        guess: RED,BLUE,GREEN,YELLOW

    This will return a json with the answer:

        {
            "black": 1,
            "white": 0
        }

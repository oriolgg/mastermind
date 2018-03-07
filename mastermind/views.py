# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from .mastermind import Mastermind

import json


colors = [ "White", "Yellow", "Red", "Gray", "Purple", "Maroon", "Lime", "Green", "Blue", "Black", ]


def new_game(request):
    """
    POST:
    Generates a new game and returns its json representation
    """
    result = {
        'res': 'OK',
        'error': '',
        'data': '',
    }

    if request.method != 'POST':
        result['res'] = 'ERROR'
        result['error'] = 'This is a POST endpoint, you cannot invoke a GET'

        return HttpResponse(json.dumps(result))

    numberOfPegs = request.POST.get('numberOfPegs', '4')
    numberOfChoices = request.POST.get('numberOfChoices', '5')

    mastermind = Mastermind()
    try:
        mastermind.createNewGame(int(numberOfPegs), int(numberOfChoices))
    except ValueError as err:
        result['res'] = 'ERROR'
        result['error'] = str(err)
        
        return HttpResponse(json.dumps(result))

    result['data'] = gameToJson(mastermind.game, False)

    return HttpResponse(json.dumps(result))


def game(request, game_id):
    """
    GET/POST:
    Returns the json representation of the specified game
    """
    result = {
        'res': 'OK',
        'error': '',
        'data': '',
    }

    mastermind = Mastermind()
    mastermind.getGame(game_id)
    if mastermind.game == None:
        result['res'] = 'ERROR'
        result['error'] = 'There is no game with id ' + str(game_id)
    else:
        result['data'] = gameToJson(mastermind.game, mastermind.isCompleted())

    return HttpResponse(json.dumps(result))


def new_guess(request, game_id):
    """
    POST:
    Creates an attempt to guess the specified game.
    Returns a json with two keys: black and white
    """
    result = {
        'res': 'OK',
        'error': '',
        'data': '',
    }

    if request.method != 'POST':
        result['res'] = 'ERROR'
        result['error'] = 'This is a POST endpoint, you cannot invoke a GET'

        return HttpResponse(json.dumps(result))

    mastermind = Mastermind()
    mastermind.getGame(game_id)

    if mastermind.game == None:
        result['res'] = 'ERROR'
        result['error'] = 'There is no game with id ' + str(game_id)

        return HttpResponse(json.dumps(result))

    # Returns an error if the game is completed, so the user cannot make more attempts on it
    if mastermind.isCompleted():
        result['res'] = 'ERROR'
        result['error'] = 'This game is completed. ' \
                    'It was solved in ' + str(mastermind.game.num_attempts) + ' attempts. ' \
                    'Its pattern was "' + patternToGuess(mastermind.game.pattern) + '"'

        return HttpResponse(json.dumps(result))

    # Checks if the guess is well-formed
    try:
        guess = request.POST.get('guess')
        guess = guessToPattern(guess)
    except ValueError as err:
        result['res'] = 'ERROR'
        result['error'] = 'Color ' + str(err) + ' is not allowed, instead use one of the following: ' + ', '.join(colors[:mastermind.game.num_choices])

        return HttpResponse(json.dumps(result))

    # Checks if the guess has the same length as the game pattern
    if len(guess) != len(mastermind.game.pattern):
        result['res'] = 'ERROR'
        result['error'] = 'The number of colors has to be ' + str(len(mastermind.game.pattern))

        return HttpResponse(json.dumps(result))

    correctValueAndPosition, correctValueNotPosition = mastermind.guess(guess)

    result = {
        'black': correctValueAndPosition,
        'white': correctValueNotPosition,
    }

    return HttpResponse(json.dumps(result))


def gameToJson(game, showPattern):
    """
    Constructs a json representation of a game, showing or not its pattern
    """
    jsonGame = {
        'id': game.id,
        'started_at': game.started_at.strftime('%Y-%m-%d %H:%M:%S'),
        'state': game.state,
        'num_pegs': game.num_pegs,
        'num_choices': game.num_choices,
        'num_attempts': game.num_attempts,
    }

    attempts = []
    for attempt in game.attempt_set.all():
        attempt = {
            'id': attempt.id,
            'guess': patternToGuess(attempt.guess),
            'black': attempt.correct_value_and_position,
            'white': attempt.correct_value_not_position,
        }
        attempts.append(attempt)
    jsonGame['attempts'] = attempts

    if showPattern:
        jsonGame['pattern'] = patternToGuess(game.pattern)

    return jsonGame


def patternToGuess(pattern):
    """
    Since the mastermind game does not know what kind of elements will be able to be choosen
    by the user (maybe colors, or emojis or anything else), we need two methods to transform
    from the user elements to the pattern that matermind understands.

    This method transforms the mastermind pattern to colors
    """
    guess = []
    for x in pattern:
        guess.append(colors[int(x)].upper())
    return ','.join(guess)


def guessToPattern(guess):
    """
    Since the mastermind game does not know what kind of elements will be able to be choosen
    by the user (maybe colors, or emojis or anything else), we need two methods to transform
    from the user elements to the pattern that matermind understands.

    This method transforms the colors to the mastermind pattern
    """
    pattern = []
    uppercaseColors = [color.upper() for color in colors]
    for x in guess.split(','):
        if x.upper() in uppercaseColors:
            pattern.append(uppercaseColors.index(x.upper()))
        else:
            raise ValueError(x)
    return ''.join(str(x) for x in pattern)

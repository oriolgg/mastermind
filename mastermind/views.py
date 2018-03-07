# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from .mastermind import Mastermind

import json


colors = [ "White", "Yellow", "Red", "Gray", "Purple", "Maroon", "Lime", "Green", "Blue", "Black", ]


def new_game(request):
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


def gameToJson(game, showPattern):
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
    guess = []
    for x in pattern:
        guess.append(colors[int(x)].upper())
    return ','.join(guess)

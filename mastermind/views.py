# -*- coding: utf-8 -*-

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .mastermind import Mastermind

import json

def new_game(request):
    mastermind = Mastermind(4, 5)
    serializedGame = serializers.serialize("json", [ mastermind.game, ])

    result = {
        'res': 'OK',
        'error': {},
        'data': serializedGame,
    }

    return HttpResponse(json.dumps(result))

def game(request, game_id):
    mastermind = Mastermind(game_id)
    serializedGame = serializers.serialize("json", [ mastermind.game, ])

    result = {
        'res': 'OK',
        'error': {},
        'data': serializedGame,
    }

    return HttpResponse(json.dumps(result))

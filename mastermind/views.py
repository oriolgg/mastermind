# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from .mastermind import Mastermind

import json

def new_game(request):
    result = {
        'res': 'OK',
        'error': {},
        'data': {
            'gameId': '',
        },
    }

    return HttpResponse(json.dumps(result))

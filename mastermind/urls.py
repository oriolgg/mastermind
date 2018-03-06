# -*- coding: utf-8 -*-

from .views import new_game

from django.urls import path

urlpatterns = [
    path('game', new_game, name='new_game'),
]

# -*- coding: utf-8 -*-

from . import views

from django.urls import path

urlpatterns = [
    path('game', views.new_game, name='new_game'),
    path('game/<int:game_id>', views.game, name='get_game'),
]

# -*- coding: utf-8 -*-

from . import views

from django.urls import path
from django.urls import re_path

urlpatterns = [
    path('game', views.new_game),
    re_path(r'^game/(?P<game_id>[0-9]+)$', views.game),
    re_path(r'^game/(?P<game_id>[0-9]+)/guess$', views.new_guess),
]

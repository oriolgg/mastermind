# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


GAME_STATES = (
    ('NEW', _(u'New')),
    ('STARTED', _(u'Started')),
    ('COMPLETED', _(u'Completed')),
)


class Game(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    pattern = models.CharField(max_length=32)
    state = models.CharField(max_length=32, choices=GAME_STATES, default='NEW')
    num_pegs = models.IntegerField(default=4)
    num_choices = models.IntegerField(default=5)
    attempts = models.IntegerField(default=0)


class Attempt(models.Model):
    attempted_at = models.DateTimeField(auto_now_add=True)
    guess = models.CharField(max_length=32)
    correct_value_and_position = models.IntegerField()
    correct_value_not_position = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

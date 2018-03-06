# -*- coding: utf-8 -*-

from random import randrange
from .models import Game, Attempt

class Mastermind:


    game = None


    def __init__(self, numberOfPegs, numberOfChoices):
        pattern = []
        for x in range(0, numberOfPegs):
            pattern.append(randrange(numberOfChoices))
        
        game = Game(pattern=pattern)
        game.save()

        self.game = game


    def guess(self, guess):
        correctValueAndPosition = 0
        correctValueNotPosition = 0

        remainingPattern = []
        remainingGuess = []

        correctValueAndPosition = sum(1 for ind, x in enumerate(self.game.pattern) if x == guess[ind])
        for ind, x in enumerate(self.game.pattern):
            if x != guess[ind]:
                remainingPattern.append(self.game.pattern[ind])
                remainingGuess.append(guess[ind])

        for i in range(len(remainingGuess)):
            if remainingGuess[i] in remainingPattern:
                correctValueNotPosition += 1
                del remainingPattern[remainingPattern.index(remainingGuess[i])]

        attempt = Attempt(guess=guess, correct_value_and_position=correctValueAndPosition, correct_value_not_position=correctValueNotPosition, game=self.game)
        attempt.save()

        return correctValueAndPosition, correctValueNotPosition


    def saveGuess(self, guess):
        return

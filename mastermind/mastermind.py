# -*- coding: utf-8 -*-

from random import randrange
from .models import Game, Attempt

class Mastermind:


    game = None


    def createNewGame(self, numberOfPegs=4, numberOfChoices=5):
        pattern = ""
        for x in range(0, numberOfPegs):
            pattern += str(randrange(numberOfChoices))
        
        self.game = Game(pattern=pattern, num_pegs=numberOfPegs, num_choices=numberOfChoices)
        self.game.save()


    def getGame(self, gameId):
        self.game = Game.objects.filter(pk=gameId).first()


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

        if correctValueAndPosition == len(self.game.pattern):
            self.game.state = 'COMPLETED'
        else:
            self.game.state = 'STARTED'
        self.game.attempts += 1
        self.game.save()
        attempt = Attempt(guess=guess, correct_value_and_position=correctValueAndPosition, correct_value_not_position=correctValueNotPosition, game=self.game)
        attempt.save()

        return correctValueAndPosition, correctValueNotPosition


    def isCompleted(self):
        return self.game.state == 'COMPLETED'

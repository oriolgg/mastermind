# -*- coding: utf-8 -*-

from random import randrange
from .models import Game, Attempt

class Mastermind:


    game = None


    def createNewGame(self, numberOfPegs=4, numberOfChoices=5):
        """
        Creates a new game with a random pattern and saves it to the database
        """
        pattern = ""
        for x in range(0, numberOfPegs):
            pattern += str(randrange(numberOfChoices))
        
        self.game = Game(pattern=pattern, num_pegs=numberOfPegs, num_choices=numberOfChoices)
        self.game.save()


    def getGame(self, gameId):
        """
        Gets a game from the database
        """
        self.game = Game.objects.filter(pk=gameId).first()


    def guess(self, guess):
        """
        Saves a guess to the database and returns the number of exact matches of value and position and
        the matches of color but not position
        """

        # counts the correct value and position elements in the guess
        correctValueAndPosition = sum(1 for ind, x in enumerate(self.game.pattern) if x == guess[ind])

        # we need to know which elements does not have the correct value and position to count the elements
        # that have the correct value but not position
        remainingPattern = []
        remainingGuess = []
        for ind, x in enumerate(self.game.pattern):
            if x != guess[ind]:
                remainingPattern.append(self.game.pattern[ind])
                remainingGuess.append(guess[ind])

        # counts the elements that have the correct value but not the correct position
        correctValueNotPosition = 0
        for i in range(len(remainingGuess)):
            if remainingGuess[i] in remainingPattern:
                correctValueNotPosition += 1
                del remainingPattern[remainingPattern.index(remainingGuess[i])]

        # if the count of correct value and position elements are the same as the length of the pattern,
        # we can say that the user has completed the game
        if correctValueAndPosition == len(self.game.pattern):
            self.game.state = 'COMPLETED'
        else:
            self.game.state = 'STARTED'
        self.game.num_attempts += 1
        self.game.save()
        attempt = Attempt(guess=guess, correct_value_and_position=correctValueAndPosition, correct_value_not_position=correctValueNotPosition, game=self.game)
        attempt.save()

        return correctValueAndPosition, correctValueNotPosition


    def isCompleted(self):
        """
        Returns true if the game is completed
        """
        return self.game.state == 'COMPLETED'

## About ##
This project explores teaching a NEAT (NeuroEvolution of Augmenting Topologies) evolving arbitrary neural network to play Blackjack. Within this repo there is a completed Blackjack game that either a user or an AI can play.

## Code Details ##
There are a couple changeable parameters in the main.py folder that will change the run experience.

DRAW_AI_GAME -> will draw out each hand when the AI model is learning. *** This will significantly slow down the learning process ***
<br>AI_RUN -> if set to False will allow user to play black jack against dealer instead of AI model learning.

## AI Details ##
For the AI I used a FeedForwardNetwork and used the players hand sum, dealers first dealt card, and the bet amount based on win / loss ratio. The higher the win ratio the more it would bet incentivizing efficiency and wins when developing its model. 
<br>The outputs consisted of hit, stay, or double down (if it is directly after being dealt the first 2 cards).
<br>
<br>For the fitness I tried utilizing just -1 for a loss and +1 for a win, but moved to be directly correlated with money lost and won. I wanted to incentivize double downs more and see if adding more parameters (like bet amount) would change the learning of the model.

## AI Results ##
Training this AI seemed to stagnate fairly quickly. Currently there is no viable strategy that the AI has come up with that consistently make money. 
The latest run can be seen in stats.png file. This came from the outputted stats from a ~80 generation run with the latest config and code. 

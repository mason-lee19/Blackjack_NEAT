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
After many tweaks to the NEAT configuration, I was able to get a NN that plays fairly good blackjack. Looking at the stats.png on average, each generation looses about 800 dollars for 100 games with a betting amount starting at 100 and adjusts as time goes on based on win loss ratio as explained in the AI details. I am happy with these results and will be adding analysis into the strategy by looking at output.csv. After finding a winner I had the that model play a large number of games to get data on the stategy the AI found.

## Summary ##
Overall I am happy with the results. I wanted to stay away from counting cards and found a strategy that rivals the average blackjack player. I believe the variablity of the game makes it difficult to find a consitently positive strategy.


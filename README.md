# NEAT-Blackjack AI

![Blackjack AI]([https://your-image-url.com/your-image.png](https://github.com/mason-lee19/Blackjack_NEAT/blob/master/stats.png))

## Overview

This project demonstrates the application of NEAT (NeuroEvolution of Augmenting Topologies) in training an AI to play the game of Blackjack. NEAT is a powerful evolutionary algorithm that evolves neural networks to perform tasks through a process resembling biological evolution.

## Contents

- [Blackjack Analysis Folder](#blackjack-analysis-folder)
- [Blackjack Folder](#blackjack-folder)
- [best.pickle](#bestpickle)
- [config.txt](#configtxt)
- [winner_ai.csv](#winner_aicsv)
- [stats.png](#statspng)


### Blackjack Analysis Folder

Contains jupyter notebook and blackjack data from Kaggle that I used for my original analysis before jumping into NEAT AI training.

### Blackjack Folder

Contains the source code for the Blackjack game. The AI is trained to play this game using NEAT.

### best.pickle

This file contains the saved neural network model of the winning AI. You can load this model to play Blackjack with the trained AI or use it for other applications.

### config.txt

The configuration file used for NEAT. It specifies the parameters and settings for the NEAT algorithm, such as population size, mutation rates, and neural network structure.

### winner_ai.csv

A CSV file containing the results of games played by the winning AI. It includes data such as the game outcome, player actions, and more.

### stats.png

A visualization of the training data, showing the AI's progress over time. This graph provides insights into the learning curve and performance improvements during training.

## AI Details

The AI in this project is built upon a FeedForwardNetwork and utilizes several key factors to make decisions during Blackjack gameplay:

- **Player's Hand Sum**: The sum of the player's current hand value.
- **Dealer's First Dealt Card**: The value of the dealer's first card, which is visible to the player.
- **Bet Amount Based on Win/Loss Ratio**: The AI adjusts its betting strategy based on its win/loss ratio. A higher win ratio incentivizes the AI to bet more, aiming for efficiency and more significant wins as it refines its model.
- **Outputs**: The AI's decisions are categorized into "hit," "stay," or "double down" (if it's directly after being dealt the first two cards).

For fitness evaluation, I initially experimented with a simple approach of assigning -1 for a loss and +1 for a win. However, I later refined the fitness function to be directly correlated with the money won or lost during gameplay. This adjustment aimed to encourage the AI to learn and favor double-down strategies and accommodate additional parameters like bet amounts.

## AI Results

After numerous iterations and tweaks to the NEAT configuration, I achieved a neural network (NN) model that demonstrates proficient Blackjack gameplay. Analyzing the `stats.png` graph, on average, each generation experiences an approximate loss of $800 over 100 games. The initial betting amount starts at $100 and adjusts dynamically based on the win-loss ratio, as explained in the AI details. These results are promising and indicate a learning AI.

I have further analyzed the AI's strategy by examining the `output.csv` file. To obtain more comprehensive insights, I had the winning model play a substantial number of games to gather data on the strategies the AI has developed.

## Summary

In summary, I am pleased with the results achieved by this AI. The project's goal was to develop a competitive Blackjack-playing AI without relying on card counting techniques. The AI's strategy approaches that of an average Blackjack player. It's important to note that the inherent variability in the game makes it challenging to find a consistently profitable strategy. This project showcases the potential of NEAT-based AI in complex decision-making tasks and provides a foundation for further exploration and optimization.



from Blackjack import Game
import os
import pickle
import neat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STARTING_BALANCE = 10000
NUMBER_OF_DECKS = 8
BET_AMOUNT = 100
GAMES_PER_CHILD = 100

# If you want the Game drawn when AI is playing
DRAW_AI_GAME = False

# AI_RUN = True: Trains NEAT algorithm and has the bot play
# AI_RUN = False: Lets either user play
AI_RUN = True

GENOME_RESULTS = []

class BlackJackGame:
    def __init__(self) -> None:
        self.game = Game(STARTING_BALANCE, NUMBER_OF_DECKS, BET_AMOUNT)

    def play_hand(self, net=None, drawGame=False, ai=False) -> int:
        """Runs a game loop to play a single hand of blackjack"""
        return self.game.game_loop(net, drawGame, AI_RUN)

def eval_genomes(genomes, config):
    results = pd.DataFrame()
    allGenomeFitness = []
    resultingBalance = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        fitness = 0
        newGame = BlackJackGame()
        for i in range(GAMES_PER_CHILD):
            fitness += newGame.play_hand(net, DRAW_AI_GAME, AI_RUN)

        temp_df = pd.DataFrame.from_dict(newGame.game.analysis_df)
        results = pd.concat([results,temp_df],ignore_index=True)

        genome.fitness = fitness

        allGenomeFitness.append(genome.fitness)
        resultingBalance.append(newGame.game.player1.playerBalance)
    
    results.to_csv('output.csv',index=False)
    
    genomeStd = np.std(allGenomeFitness)
    genomeAvg = sum(allGenomeFitness)/len(allGenomeFitness)
    genomeMax = max(allGenomeFitness)
    avgBalance = sum(resultingBalance)/len(resultingBalance)
    maxBalance = max(resultingBalance)
    minBalance = min(resultingBalance)

    GENOME_RESULTS.append([genomeAvg,genomeMax,genomeStd,avgBalance,maxBalance,minBalance])
    plt.figure(figsize=(10,10))
    plt.subplot(3,1,1)
    plt.plot(plot_data(GENOME_RESULTS,0),label='Avg Genome Fitness')
    plt.plot(plot_data(GENOME_RESULTS,1),label='Max Genome Fitness')
    plt.ylabel("Fitness")
    plt.title("Population Fitness Over Generations")
    plt.legend()
    plt.subplot(3,1,2)
    plt.plot(plot_data(GENOME_RESULTS,2), label='Genome Fitness STD')
    plt.ylabel("Fitness STD")
    plt.legend()
    plt.subplot(3,1,3)
    plt.plot(plot_data(GENOME_RESULTS,3), label='Avg Genome balance')
    plt.plot(plot_data(GENOME_RESULTS,4), label='Max Balance')
    plt.plot(plot_data(GENOME_RESULTS,5), label='MinBalance')
    plt.xlabel("Generation")
    plt.ylabel("Avg Balance")
    plt.legend()
    plt.savefig("stats.png")
    plt.pause(0.5)
    plt.close()

def plot_data(dataList:list,colIdx) -> list:
    output = []
    for idx in range(len(dataList)):
        x = dataList[idx][colIdx] # extract the first column
        output.append(x)

    return output


def run_neat(config):
    genome_results = []
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer)
    plt.ion()
    plt.show()
    winner = p.run(eval_genomes)
    with open("best.pickle","wb") as f:
        pickle.dump(winner,f)

def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner,config)

    newGame = BlackJackGame()
    for i in range(50000):
        newGame.play_hand(winner_net, DRAW_AI_GAME)

    temp_df = pd.DataFrame.from_dict(newGame.game.analysis_df)
    temp_df.to_csv('winner_ai.csv',index=False)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    if AI_RUN:
        run_neat(config)
        test_best_network(config)
    else:
        run = True
        game = BlackJackGame()
        while run:
            game.play_hand(None, True)
            


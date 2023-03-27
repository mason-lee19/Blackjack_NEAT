from Blackjack import Game
import os
import pickle
import neat
import matplotlib.pyplot as plt
import numpy as np

STARTING_BALANCE = 10000
NUMBER_OF_DECKS = 4
BET_AMOUNT = 100
GAMES_PER_CHILD = 50

# If you want the Game drawn when AI is playing
DRAW_AI_GAME = False

# AI_RUN = True: Trains NEAT algorithm and has the bot play
# AI_RUN = False: Lets user play blackjack against dealer
AI_RUN = True

GENOME_RESULTS = []

class BlackJackGame:
    def __init__(self) -> None:
        self.game = Game(STARTING_BALANCE, NUMBER_OF_DECKS, BET_AMOUNT)

    def play_hand(self, net=None, drawGame=False, ai=False) -> int:
        """Runs a game loop to play a single hand of blackjack"""
        return self.game.game_loop(net, drawGame, AI_RUN)

def eval_genomes(genomes, config):
    allGenomeFitness = []
    resultingBalance = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        fitness = 0
        newGame = BlackJackGame()
        for i in range(GAMES_PER_CHILD):
            fitness += newGame.play_hand(net, DRAW_AI_GAME, AI_RUN)

        genome.fitness = fitness

        allGenomeFitness.append(genome.fitness)
        resultingBalance.append(newGame.game.player1.playerBalance)
    
    genomeStd = np.std(allGenomeFitness)
    genomeAvg = sum(allGenomeFitness)/len(allGenomeFitness)
    avgBalance = sum(resultingBalance)/len(resultingBalance)
    maxBalance = max(resultingBalance)
    minBalance = min(resultingBalance)

    GENOME_RESULTS.append([genomeAvg,genomeStd,avgBalance,maxBalance,minBalance])
    plt.figure(figsize=(10,10))
    plt.subplot(3,1,1)
    plt.plot(plot_data(GENOME_RESULTS,0),label="Avg Genome Fitness")
    plt.ylabel("Fitness")
    plt.title("Population Fitness Over Generations")
    plt.legend()
    plt.subplot(3,1,2)
    plt.plot(plot_data(GENOME_RESULTS,1), label='Genome Fitness STD')
    plt.ylabel("Fitness STD")
    plt.legend()
    plt.subplot(3,1,3)
    plt.plot(plot_data(GENOME_RESULTS,2), label='Avg Genome balance')
    plt.plot(plot_data(GENOME_RESULTS,3), label='Max Balance')
    plt.plot(plot_data(GENOME_RESULTS,4), label='MinBalance')
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

    game = BlackJackGame()
    for i in range(100):
        game.play_hand(winner_net, DRAW_AI_GAME)


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
            


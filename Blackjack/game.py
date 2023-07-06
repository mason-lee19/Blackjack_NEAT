from .player import Dealer, TablePlayer
from .deck import Deck
import os

class Game():

    def __init__(self, startingBalance, numDecks, betAmount):
        self.playerWins: int = 0
        self.playerLosses: int = 0
        self.startingBalance:int  = startingBalance
        self.playerBalance: int = startingBalance
        self.gamesPlayed: int = 0

        self.dealer: Dealer = Dealer()
        self.player1: TablePlayer = TablePlayer(startingBalance)

        self.startingBetAmount: int = betAmount
        self.betAmount: int = betAmount

        self.deck = Deck(numDecks)

        self.analysis_df = {
            'playerCard1': [],
            'playerCard2': [],
            'playerCard3': [],
            'playerCard4': [],
            'playerCard5': [],
            'dealerCard1': [],
            'dealerCard2': [],
            'dealerCard3': [],
            'dealerCard4': [],
            'dealerCard5': [],
            'playerHandSum': [],
            'dealerHandSum': [],
            'cardsLeft': [],
            'result': [],
        }

    def game_loop(self, net, draw:bool=False, ai:bool=True) -> int:
        """ 
        Executes a single hand of black jack
        Inputs: 
        net: AI NEAT FeedForward Network
        draw: Draw the hands that are being played
        ai: True if you want the AI to play False to let you play

        output:
        Game result: -1 for a Loss, 1 for a win and 0 for a push
        """

        self.deck.check_deck_size()
        self.betAmount = self.startingBetAmount * ((self.playerWins+1)/(self.gamesPlayed+1))

        if draw:
            print(f'You have ${self.player1.playerBalance}')

        for i in range(2):
            self.dealer.get_card(self.deck.deal_card())
            self.player1.get_card(self.deck.deal_card())

        self.dealer.check_for_ace_bust()
        self.player1.check_for_ace_bust()

        if draw:
            self.draw_game()

        # Real player's move
        if not ai:
            self.player1.get_move_input()

            if self.player1.move.lower() == 'dd':
                self.handle_double_down(draw)

            elif self.player1.move.lower() == 'hit':
                while self.player1.move.lower() == 'hit':
                    output = self.handle_player_hit(False, draw)
        
        # AI move
        else:
            inputs = (self.player1.handSum, self.dealer.handValues[0],self.betAmount)
            output = net.activate(inputs)
            decision = output.index(max(output))
            
            if self.player1.handSum < 12:
                if output[0] < output[1]: decision = 0
                else: decision = 1

            if decision == 0 and len(self.player1.hand) == 2:
                self.handle_double_down(draw)

            elif decision == 1 or self.player1.handSum < 12:
                while decision == 1 or self.player1.handSum < 12:
                    decision = self.handle_ai_hit(net,draw)
                

        # Dealer's move
        self.dealer.check_dealer_move()

        while self.dealer.move.lower() == 'hit':
            self.handle_player_hit(True,draw)

        result = self.player1.calc_results(self.betAmount, self.dealer.handSum)

        self.update_stats(result, draw, ai)

        self.add_results(result)

        self.player1.reset_hand()
        self.dealer.reset_hand()

        if result == 'Loss':
            return -self.betAmount
        elif result == 'Win':
            return self.betAmount
        else:
            return self.betAmount * 0.5

    def add_results(self, result) -> None:
        for i in range(5):
            player_column = 'playerCard' + str(i+1)
            dealer_column = 'dealerCard' + str(i+1)
            try:
                self.analysis_df[player_column].append(str(self.player1.handValues[i]))
            except:
                self.analysis_df[player_column].append(0)

            try:
                self.analysis_df[dealer_column].append(str(self.dealer.handValues[i]))
            except:
                self.analysis_df[dealer_column].append(0)
        self.analysis_df['playerHandSum'].append(self.player1.handSum)
        self.analysis_df['dealerHandSum'].append(self.dealer.handSum)
        self.analysis_df['cardsLeft'].append(len(self.deck.cardStack))
        self.analysis_df['result'].append(result)

    def handle_player_hit(self, dealer:bool, draw:bool) -> None:
        '''Handle Player Hit'''
        if not dealer:
            self.player1.get_card(self.deck.deal_card())
            self.player1.check_for_ace_bust()
            if draw: self.draw_game()
            self.player1.get_move_input()
        else:
            self.dealer.get_card(self.deck.deal_card())
            self.dealer.check_for_ace_bust()
            if draw: self.draw_game()
            self.dealer.check_dealer_move()

    def handle_ai_hit(self,net,draw) -> int:
        '''Handle AI Hit'''
        self.player1.get_card(self.deck.deal_card())
        self.player1.check_for_ace_bust()

        if draw: self.draw_game()
        if self.player1.check_ai_bust(): return 0

        inputs = (self.player1.handSum, self.dealer.handValues[0], self.betAmount)
        output = net.activate(inputs)
        return output.index(max(output))
    

    def handle_double_down(self, draw:bool) -> None:
        '''Handle Player Double Down'''
        self.betAmount = self.player1.double_down(self.betAmount)
        self.player1.get_card(self.deck.deal_card())
        self.player1.check_for_ace_bust()
        if draw: self.draw_game()

    def update_stats(self, results:str, draw:bool, ai:bool) -> None:
        '''Update win and losses for hand played'''
        if results == 'Win' or results == 'Natural Win':
            self.playerWins+=1
            if draw: print('****YOU WON****')
        elif results == 'Loss':
            self.playerLosses+=1
            if draw: print('****YOU LOST****')
        else:
            if draw: print('*****PUSH****')

        # We want to pause to see if we won or lost if it's not ai
        if not ai: input()

        self.gamesPlayed += 1

    def draw_game(self) -> None:
        '''Draw cards during play'''
        os.system('clear')
        print(f'Current Balance: {self.player1.playerBalance}')
        print(f'Current Bet Amount: ${self.betAmount}')
        print('\n')
        print(f'Dealer has {self.dealer.handSum}: ')
        self.deck.print_hand(self.dealer.hand)
        print(f'Player has {self.player1.handSum}: ')
        self.deck.print_hand(self.player1.hand)

    def reset(self) -> None:
        '''Reset hands and player stats'''
        self.dealer.reset_hand()
        self.player1.reset_hand()
        self.playerWins = 0
        self.playerLosses = 0
        self.playerBalance = self.startingBalance
        self.gamesPlayed = 0
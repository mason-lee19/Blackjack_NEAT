from .deck import Deck

class Player():
    def __init__(self) -> None:
        self.handSum: int = 0
        self.hand: list = []
        self.handValues: list = []
        self.move: list = []

    def get_card(self,card) -> None:
        '''Get card for player'''
        self.hand.append(card[0] + ' of ' + card[1])
        self.handValues.append(card[2])
        self.handSum += card[2]

    def check_for_ace_bust(self) -> None:
        '''Check if player has over 21 and if has ace turn value from 11 to 1'''
        if self.handSum > 21 and 11 in self.handValues:
            for idx, values in enumerate(self.handValues):
                if values == 11:
                    self.handValues[idx] = 1
                    self.handSum = sum(self.handValues)
                    break

    def reset_hand(self) -> None:
        '''Reset hand'''
        self.handSum = 0
        self.handValues = []
        self.hand = []


class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    def check_dealer_move(self) -> None:
        '''Dealer logic to check for next move'''
        if self.handSum < 17:
            self.move = 'hit'
        elif self.handSum > 21:
            self.move = 'bust'
        else:
            self.move = 'stay'

class TablePlayer(Player):
    def __init__(self, startingMoney: int) -> None:
        super().__init__()
        self.playerBalance:int = startingMoney

    def get_bet_amount(self) -> int:
        '''Player Input for bet amount'''
        bet_amount = int(input('Bet amount: '))
        while bet_amount < 1 or bet_amount > self.playerBalance:
            bet_amount = int(input('Please input a working bet amount: '))

        return bet_amount

    def get_move_input(self) -> None:
        '''Player move input'''
        if self.handSum > 21:
            self.move = 'bust'
        elif self.handSum == 21:
            self.move = 'stay'
        elif len(self.hand) == 2:
            self.move = input('Hit, Stay, or DD: ')
            while self.move.lower() != 'hit' and self.move.lower() != 'stay' and self.move.lower() != 'dd':
                self.move = input('Hit, Stay, or DD: ')
        else:
            self.move = input('Hit or Stay: ')
            while self.move.lower() != 'hit' and self.move.lower() != 'stay':
                self.move = input('Input hit or stay: ')

    def check_ai_bust(self) -> bool:
        '''Check if ai busted to force out of hit loop'''
        if self.handSum > 21:
            return True
        return False
           
    def double_down(self, betAmount) -> int:
        '''Double bet amount on a double down'''
        dd_bet_amount = betAmount * 2
        return dd_bet_amount

    def calc_results(self,betAmount: int, dealerHandSum: int) -> str:
        '''Calculate game results'''
        result = ''

        if (self.handSum > 21) or (dealerHandSum <= 21 and dealerHandSum > self.handSum):
            self.playerBalance = self.playerBalance - betAmount
            result = 'Loss'
        elif self.handSum == 21 and self.handSum == 2:
            self.playerBalance = self.playerBalance + betAmount * 1.5
            result = 'Natural Win'
        elif (self.handSum <= 21 and dealerHandSum < self.handSum) or (dealerHandSum > 21 and self.handSum <= 21):
            self.playerBalance = self.playerBalance + betAmount
            result = 'Win'
        else:
            result = 'Push'

        return result
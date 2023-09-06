import random

class Deck():
    def __init__(self, numDecks:int) -> None:
        self.ranks: list = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.suits: list = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.values: dict = {"Ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10}
        self.cardStack: list = []
        self.numDecks: int = numDecks
        self.deckCount: int = 0
        self.totalCards: int = numDecks * 52
        
        self.create_new_deck()
        self.shuffle_deck()

    def create_new_deck(self) -> None:
        ''''Create new deck'''
        self.cardStack = []
        self.count = 0
        for i in range(self.numDecks):
            for rank in self.ranks:
                for suit in self.suits:
                    card = [rank, suit, self.values.get(rank)]
                    self.cardStack.append(card)

    def shuffle_deck(self) -> None:
        '''Randomize deck'''
        random.shuffle(self.cardStack)

    def deal_card(self) -> str:
        '''Deal card to player'''
        card = self.cardStack.pop()
        # Keep track of count
        # 2-6 = +1
        # 7-9 = 0
        # 10-11 = -1
        if card[2] >= 10:
            self.count-=1
        elif card[2] <= 6:
            self.count+=1
        return card

    def check_deck_size(self) -> None:
        '''Check if deck needs to be reshuffled'''
        if len(self.cardStack) < (self.totalCards/2):
            self.create_new_deck()
            self.shuffle_deck()

    def make_card(self, card) -> list:
        '''Make card art for printing'''
        pcarddisplay = [] 
        pcarddisplay.append("┌─────────┐")
        pcarddisplay.append("│{}{}. . .│")
        pcarddisplay.append("│. . . . .│")
        pcarddisplay.append("│. . . . .│")
        pcarddisplay.append("│. . {}. .│")
        pcarddisplay.append("│. . . . .│")
        pcarddisplay.append("│. . . . .│")
        pcarddisplay.append("│. . .{}{}│")
        pcarddisplay.append("└─────────┘")

        x = ("│.", card[:1], ". . . .│")
        pcarddisplay[1] = "".join(x)

        x = ("│. . . .", card[:1], ".│")
        pcarddisplay[7] = "".join(x)

        if "Diamonds" in card:
            pcarddisplay[4] = "│. . ♦ . .│"
        if "Clubs" in card:
            pcarddisplay[4] = "│. . ♣ . .│"
        if "Hearts" in card:
            pcarddisplay[4] = "│. . ♥ . .│"
        if "Spades" in card:
            pcarddisplay[4] = "│. . ♠ . .│"

        return pcarddisplay

    def print_hand(self, playerHand) -> None:
        '''Print cards'''
        print('\n'.join(map('  '.join, zip(*(self.make_card(c) for c in playerHand)))))



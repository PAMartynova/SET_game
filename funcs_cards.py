from itertools import product
import random as rn


colors = ['red', 'green', 'purple']
shapes = ['rhombus', 'oval', 'vawe']
fullness = ['full', 'shaded', 'empty']
amounts = ['1', '2', '3']

class Card:
    def __init__(self, card):
        self.color = card[0]
        self.shape = card[1]
        self.fullness = card[2]
        self.amount = card[3]
        try:
            #self.pict = fr"C:\Users\wowwh\PROJECTS\set-project\cards\{card[0][0]}-{card[1][0]}-{card[2][0]}-{card[3][0]}.png"
            self.pict = fr"cards\{card[0][0]}-{card[1][0]}-{card[2][0]}-{card[3][0]}.png"
        except:
            self.pict = r"cards\empty.png"
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.color == other.color and
                self.shape == other.shape and
                self.fullness == other.fullness and 
                self.amount == other.amount)
        else:
            return NotImplemented


def check_set(card1, card2, card3):
    """Check if 3 cards are the SET"""
    if (card1.color == card2.color == card3.color or card1.color != card2.color != card3.color) and (card1.shape == card2.shape == card3.shape or card1.shape != card2.shape != card3.shape) and (card1.fullness == card2.fullness == card3.fullness or card1.fullness != card2.fullness != card3.fullness) and (card1.amount == card2.amount == card3.amount or card1.amount != card2.amount != card3.amount):
        return True
    return False


def new_cards():
    """return list of cards - instances of Card class"""
    cards = []
    for c in rn.sample(list(product(colors, shapes, fullness, amounts)), 81):
        card = Card(c)
        cards.append(card)
    return cards


def find_set(cards):
    """Check if there is a set in list of cards. Return set of 3 instances of Card class or None"""
    for i, card1 in enumerate(cards):
        for card2 in cards[i+1:]:
            card3 = find_third(card1, card2)
            if card3 in cards:
                return(card1, card2, card3)
            
    return None


def find_third(card1, card2):
    """Take 2 instances on Card class, return instance of Card class - missing set element"""
    third_card = Card(('0', '0', '0', '0'))
    if card1.color == card2.color:
        third_card.color = card1.color
    else:
        third_card.color = next(filter(lambda i: i not in [card1.color, card2.color], colors))
    if card1.shape == card2.shape:
        third_card.shape = card1.shape
    else:
        third_card.shape = next(filter(lambda i: i not in [card1.shape, card2.shape], shapes))
    if card1.fullness == card2.fullness:
        third_card.fullness = card1.fullness
    else:
        third_card.fullness = next(filter(lambda i: i not in [card1.fullness, card2.fullness], fullness))
    if card1.amount == card2.amount:
        third_card.amount = card1.amount
    else:
        third_card.amount = next(filter(lambda i: i not in [card1.amount, card2.amount], amounts))
    third_card.pict = fr"cards\{third_card.color[0]}-{third_card.shape[0]}-{third_card.fullness[0]}-{third_card.amount[0]}.png"
    return third_card
    






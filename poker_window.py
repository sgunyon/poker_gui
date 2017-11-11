#! /usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from score import Score
from cards import *


class PokerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainWidget = QWidget(self)  # dummy to contain the layout manager
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Poker')

        self.grid = QGridLayout()
        self.mainWidget.setLayout(self.grid)

        # The five cards: each has a rank and a suit.
        self.hand_ranks = [None, None, None, None, None]
        self.hand_suits = [None, None, None, None, None]
        self.score_ranks = []
        self.score_suits = []

        self.deck = Deck()
        self.deck.shuffle()

        # Create the labels for the card ranks and suits:
        for i in range(0, len(self.hand_ranks)):
            self.hand_ranks[i] = QLabel()
            self.grid.addWidget(self.hand_ranks[i], 0, i)

            self.hand_suits[i] = QLabel()
            self.grid.addWidget(self.hand_suits[i], 1, i)

        # "Deal" button
        self.dealbutton = QPushButton("Deal")
        self.grid.addWidget(self.dealbutton, 2, 0)
        self.dealbutton.clicked.connect(self.deal_new_hand)

        self.evalbutton = QPushButton("Evaluate")
        self.grid.addWidget(self.evalbutton, 2, 2)
        self.evalbutton.clicked.connect(self.eval_hand)

        # Quit button
        self.quitbutton = QPushButton("Quit")
        self.grid.addWidget(self.quitbutton, 2, 4)
        self.quitbutton.clicked.connect(self.close)

        # Images for the suits:
        self.suitpics = ["images/diamond.png", "images/spade.png", "images/heart.png", "images/club.png"]
        self.suitpixmaps = [None, None, None, None]

        # Read in the suit pixmaps
        for i in range(0, len(self.suitpics)):
            self.suitpixmaps[i] = QPixmap(self.suitpics[i])

        self.font = QFont("", 0, QFont.Bold, False)
        self.font.setPointSize(self.font.pointSize() * 2)

        # Create the labels for the card ranks and suits:
        for i in range(0, len(self.hand_ranks)):
            self.hand_ranks[i].setFont(self.font)
            self.hand_ranks[i].setAlignment(Qt.AlignCenter)

    def deal_new_hand(self):

        self.deck = Deck()
        self.deck.shuffle()
        self.score_ranks = []
        self.score_suits = []
        for i in range(0, len(self.hand_ranks)):
            card = self.deck.deal_card()

            self.hand_ranks[i].setText(card.rank.__str__())
            self.score_ranks.append(card.rank.value)
            self.score_suits.append(card.suit.value)

            if self.suitpixmaps[card.suit.value].isNull():
                self.hand_suits[i].setText(card.suit.value)
            else:
                self.hand_suits[i].setPixmap(self.suitpixmaps[card.suit.value])

    def eval_hand(self):
        score = Score(self.score_suits, self.score_ranks)
        score.eval_hand()

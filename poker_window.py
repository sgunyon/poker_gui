#! /usr/bin/python

import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from score import Score



class PokerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainWidget = QWidget(self)  # dummy to contain the layout manager
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Poker')

        self.grid = QGridLayout()
        self.mainWidget.setLayout(self.grid)

        # The five cards: each has a rank and a suit.
        self.ranks = [None, None, None, None, None]
        self.suits = [None, None, None, None, None]
        self.score_ranks = []
        self.score_suits = []

        # Possible suits:
        self.suitnames = ["Diamonds", "Spades", "Hearts", "Clubs"]

        # Possible ranks:
        self.ranknames = ["2", "3", "4", "5", "6", "7", "8",
                          "9", "10", "J", "Q", "K", "A"]

        # Create the labels for the card ranks and suits:
        for i in range(0, len(self.ranks)):
            self.ranks[i] = QLabel()
            self.grid.addWidget(self.ranks[i], 0, i)

            self.suits[i] = QLabel()
            self.grid.addWidget(self.suits[i], 1, i)

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
        for i in range(0, len(self.ranks)):
            self.ranks[i].setFont(self.font)
            self.ranks[i].setAlignment(Qt.AlignCenter)

    def deal_new_hand(self):
        self.score_ranks = []
        self.score_suits =  []
        for i in range(0, 5):
            rank = random.randint(0, 12)
            self.ranks[i].setText(self.ranknames[rank])
            self.score_ranks.append(int(rank)+2)

            suit = random.randint(0, 3)
            self.score_suits.append(self.suitnames[suit])
            if self.suitpixmaps[suit].isNull():
                self.suits[i].setText(self.suitnames[suit])
            else:
                self.suits[i].setPixmap(self.suitpixmaps[suit])

    def eval_hand(self):
        """
        for i in self.score_suits:
            print(i)
        for i in self.score_ranks:
            print(i)
        """
        score = Score(self.score_suits, self.score_ranks)
        score.eval_hand()
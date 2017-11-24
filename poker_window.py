#! /usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from score import Score
from cards import *


class PokerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Poker Hand Evaluation')

        self.grid = QGridLayout()
        self.mainWidget.setLayout(self.grid)

        # Create lists
        self.hand_ranks = [None, None, None, None, None]
        self.hand_suits = [None, None, None, None, None]
        self.score_ranks = []
        self.score_suits = []
        self.suitpixmaps = [None, None, None, None]

        # Create and shuffle deck
        self.prep_deck()
        
        # Create QPixMap objects and map images/fonts to them
        self.add_card_styling()
        
        # Create QLabels for the cards and add them, as widgets, to the grid
        self.populate_card_window()
        
        # Create the buttons used to interact with the window
        self.create_buttons()
        
        # Create the text box for displaying messages
        self.create_textbox()
        self.textbox.setText("Press Deal")

    def prep_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def add_card_styling(self):
        self.suitpics = ["images/spade.png", "images/club.png", "images/heart.png", "images/diamond.png"]

        for i in range(0, len(self.suitpics)):
            self.suitpixmaps[i] = QPixmap(self.suitpics[i])

        self.font = QFont("", 0, QFont.Bold, False)
        self.font.setPointSize(self.font.pointSize() * 2)

    def populate_card_window(self):
        for i in range(0, len(self.hand_ranks)):
            self.hand_ranks[i] = QLabel()
            self.grid.addWidget(self.hand_ranks[i], 1, i)
            self.hand_ranks[i].setFont(self.font)
            self.hand_ranks[i].setAlignment(Qt.AlignCenter)

            self.hand_suits[i] = QLabel()
            self.grid.addWidget(self.hand_suits[i], 2, i)

    def create_buttons(self):
        self.deal_button = QPushButton("Deal")
        self.grid.addWidget(self.deal_button, 3, 0)
        self.deal_button.clicked.connect(self.deal_new_hand)

        self.trade_button = QPushButton("Trade-in")
        self.trade_button.setDisabled(True)
        self.grid.addWidget(self.trade_button, 3, 1)
        self.trade_button.clicked.connect(self.trade_cards)

        self.eval_button = QPushButton("Evaluate")
        self.eval_button.setDisabled(True)
        self.grid.addWidget(self.eval_button, 3, 2)
        self.eval_button.clicked.connect(self.evaluate_hand)

        self.quitbutton = QPushButton("Quit")
        self.grid.addWidget(self.quitbutton, 3, 4)
        self.quitbutton.clicked.connect(self.close)

        self.keep0 = QPushButton("Keep")
        self.keep1 = QPushButton("Keep")
        self.keep2 = QPushButton("Keep")
        self.keep3 = QPushButton("Keep")
        self.keep4 = QPushButton("Keep")
        self.keep_button_list = [self.keep0, self.keep1, self.keep2, self.keep3, self.keep4]
        count = 0
        for button in self.keep_button_list:
            button.setCheckable(True)
            button.clicked.connect(lambda: self.toggle_trade(button))
            button.setDisabled(True)
            self.grid.addWidget(button, 0, count)
            count += 1

    def create_textbox(self):
        self.textbox = QTextEdit()
        self.textbox.setMaximumHeight(50)
        self.textbox.setFont(self.font)
        self.grid.addWidget(self.textbox, 4, 0, 1, 0)

    def deal_new_hand(self):
        self.prep_deck()
        self.score_ranks = []
        self.score_suits = []
        for i in range(0, len(self.hand_ranks)):
            self.deal_new_card(i)
        self.reset_window()

    def deal_new_card(self, index):
        card = self.deck.deal_card()

        self.hand_ranks[index].setText(card.rank.__str__())

        self.score_ranks.insert(index, card.rank.value)
        self.score_suits.insert(index, card.suit.value)

        if self.suitpixmaps[card.suit.value].isNull():
            self.hand_suits[index].setText(card.suit.value)
        else:
            self.hand_suits[index].setPixmap(self.suitpixmaps[card.suit.value])

    def evaluate_hand(self):
        score = Score(self.score_suits, self.score_ranks)
        self.textbox.setText(score.evaluate_hand())
        self.enable_button(self.deal_button)
        self.disable_button(self.eval_button)

    def update_second_hand(self, index):
        self.score_ranks.remove(self.score_ranks[index])
        self.score_suits.remove(self.score_suits[index])
        self.deal_new_card(index)

    def trade_cards(self):
        self.disable_button(self.trade_button)
        self.enable_button(self.eval_button)
        for button in self.keep_button_list:
            if button.isChecked() == False:
                update_index = self.keep_button_list.index(button)
                self.update_second_hand(update_index)
            self.disable_button(button)
        return self.textbox.setText("Traded cards")

    def enable_button(self, button):
        button.setDisabled(False)
        button.setFlat(False)

    def disable_button(self, button):
        button.setDisabled(True)
        button.setFlat(True)
        
    def toggle_trade(self, button):
        if button.isChecked() == True:
            button.setDisabled(False)
            button.setFlat(False)
        self.disable_button(self.deal_button)

    def reset_window(self):
        self.textbox.clear()
        self.enable_button(self.trade_button)
        self.disable_button(self.eval_button)
        for button in self.keep_button_list:
            self.enable_button(button)
            button.setChecked(False)

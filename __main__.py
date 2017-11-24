#!/usr/bin.python

from poker_window import PokerWindow
from PyQt5.QtWidgets import *

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PokerWindow()

    win.show()
    app.exec_()

#!/usr/bin/env python3

from gui import gui
from calculate import calculate
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = gui.GUI()
    gui.setOnCalculationStart(calculate)
    gui.show()
    sys.exit(app.exec_())
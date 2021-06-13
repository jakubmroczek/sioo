#!/usr/bin/env python3

from gui import gui
from calculate import calculate
from multi_dimensional_calculation import multidimensional_calculation
from constrained_calcluation import constrained_caluclation
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = gui.GUI()
    gui.setOnOneDimensionalCalculationStart(calculate)
    # gui.setOnMulitiDimensionalCalcualtionStartCallback(multidimensional_calculation)
    gui.setOnMulitiDimensionalCalcualtionStartCallback(constrained_caluclation)
    gui.show()
    sys.exit(app.exec_())
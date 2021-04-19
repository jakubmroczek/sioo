import traceback

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QComboBox, QLineEdit,
                             QPushButton, QLabel, QMessageBox)

from function import FunctionInterval
from program_arguments import ProgramArguments, OptimizerType


class MuliDimensionalFunctionGUI:


    def add_widgets_to_layout(self, layout, rowIndex):
        '''
        This method is called by the GUI class. The layout object is expected to be of QGridLayout.
        '''
        functionLabel = QLabel('Function:')


        layout.addWidget(functionLabel, rowIndex + 0, 0, 1, 1)
        layout.addWidget(self.functionLabel, rowIndex + 0, 1, 1, 1)

        layout.addWidget(self.runButton, rowIndex + 1, 0, 1, 1)

    def __init__(self):
        self.functionLabel = QLineEdit('x ** 2 - 2 * x - 10 + y + y ** 2')

        self.runButton = QPushButton('Calculate!')

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        programArguments = self._getProgramArguments()

        try:
            result = self.onCalculationStartCallback(programArguments)
            self._plot(result)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            text = f'{str(e)}\n Traceback: "{traceback.print_exc()}"'
            msg.setText(text)
            msg.exec()
        except:
            print(f'Caught unsupported exception!\n Traceback: "{traceback.print_exc()}"')

    def _plot(self, result):
        print('plotting a beautiful function')

    def _getProgramArguments(self):
        print('returning empyt args')
        return ()
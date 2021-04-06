from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                             QPushButton)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from program_arguments import ProgramArguments, OptimizerType
from function import FunctionRange

class GUI(QDialog):
    BISECTION = 'Bisection'
    GOLDEN_SECTION_SEARCH = 'Golden-section search'
    SCIPY_BISECTION = 'SciPy Bisection'
    SCIPTY_GOLDEN_SECITION_SEARCH = 'Sci-Py Golden-section search'

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        # Plot
        self.graphWidget = pg.PlotWidget()

        #
        self.functionLabel = QLineEdit('function')
        self.functionLowPointLabel = QLineEdit('domain start')
        self.functionHighLabel = QLineEdit('domain end')
        self.optimizerComboBox = QComboBox()
        self.optimizerComboBox.addItems([self.BISECTION, self.GOLDEN_SECTION_SEARCH, self.SCIPY_BISECTION, self.SCIPTY_GOLDEN_SECITION_SEARCH])
        self.runButton = QPushButton('Calculate!')

        layout = QGridLayout()
        layout.addWidget(self.functionLabel, 0, 0, 1, 2)
        layout.addWidget(self.functionLowPointLabel, 1, 0, 1, 2)
        layout.addWidget(self.functionHighLabel, 2, 0, 1, 2)
        layout.addWidget(self.optimizerComboBox, 3, 0, 1, 2)
        layout.addWidget(self.runButton, 4, 0, 1, 2)
        layout.addWidget(self.graphWidget, 5, 0, 1, 2)

        layout.setRowStretch(5, 1)

        self.setLayout(layout)

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        programArguments = self._getProgramArguments()
        self.onCalculationStartCallback(programArguments)

    def _getProgramArguments(self):
        arguments = ProgramArguments()
        arguments.expression = self.functionLabel.text()
        arguments.functionRange = FunctionRange(float(self.functionLowPointLabel.text()),
                                                float(self.functionHighLabel.text()))

        optimzerType = str(self.optimizerComboBox.currentText())

        if optimzerType == self.BISECTION:
            arguments.optimizerType = OptimizerType.BISECTION
        elif optimzerType == self.GOLDEN_SECTION_SEARCH:
            arguments.optimizerType = OptimizerType.GOLDEN_SECTION_SEARCH
        elif optimzerType == self.SCIPY_BISECTION:
            arguments.optimizerType = OptimizerType.SCIPY_BISECTION
        else:
            arguments.optimizerType = OptimizerType.SCIPY_GOLDEN_SECTION_SEARCH

        return arguments

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                             QPushButton, QLabel, QMessageBox)
import numpy as np
from PyQt5 import QtCore
import pyqtgraph as pg
from program_arguments import ProgramArguments, OptimizerType
from function import FunctionInterval
import traceback

class OneDimensionalFunctionGUI:
    BISECTION = 'Bisection'
    GOLDEN_SECTION_SEARCH = 'Golden-section search'
    SCIPY_BISECTION = 'SciPy Bisection'
    SCIPTY_GOLDEN_SECITION_SEARCH = 'Sci-Py Golden-section search'


    def add_widgets_to_layout(self, layout, rowIndex):
        '''
        This method is called by the GUI class. The layout object is expected to be of QGridLayout.
        '''
        functionLabel = QLabel('Function:')
        intervalStartLabel = QLabel('Interval start:')
        intervalEndLabel = QLabel('Interval end:')
        maxIterationsLabel = QLabel('Max iterations:')
        xtolLabel = QLabel('Xtol:')
        unimodalityCheckPointsLabel = QLabel('Unimodality-check points number:')
        exhaustiveSerachPoints = QLabel('Exhaustive search points number:')

        layout.addWidget(functionLabel, rowIndex + 0, 0, 1, 1)
        layout.addWidget(self.functionLabel, rowIndex + 0, 1, 1, 1)

        layout.addWidget(intervalStartLabel, rowIndex + 1, 0, 1, 1)
        layout.addWidget(self.functionLowPointLabel, rowIndex + 1, 1, 1, 1)

        layout.addWidget(intervalEndLabel, rowIndex + 2, 0, 1, 2)
        layout.addWidget(self.functionHighLabel, rowIndex + 2, 1, 1, 1)

        layout.addWidget(maxIterationsLabel, rowIndex + 3, 0, 1, 1)
        layout.addWidget(self.maxIterationsEdit, rowIndex + 3, 1, 1, 1)

        layout.addWidget(xtolLabel, rowIndex + 4, 0, 1, 1)
        layout.addWidget(self.xtolEdit, rowIndex + 4, 1, 1, 1)

        # Unimodality check
        layout.addWidget(unimodalityCheckPointsLabel, rowIndex + 5, 0, 1, 1)
        layout.addWidget(self.unimodalityCheckPointsEdit, rowIndex + 5, 1, 1, 1)

        # Exhaustive search
        layout.addWidget(exhaustiveSerachPoints, rowIndex + 6, 0, 1, 1)
        layout.addWidget(self.exhaustiveSerachEdit, rowIndex + 6, 1, 1, 1)

        layout.addWidget(self.optimizerComboBox, rowIndex + 7, 0, 1, 2)
        layout.addWidget(self.runButton, rowIndex + 8, 0, 1, 2)
        layout.addWidget(self.graphWidget, rowIndex + 9, 0, 1, 2)

        layout.setRowStretch(5, 1)

    def __init__(self):
        # Plot
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('#7C7C7C')
        self.graphWidget.showGrid(x = True, y = True, alpha = 0.8)

        self.functionLabel = QLineEdit('x ** 2 - 2 * x - 10')
        self.functionLowPointLabel = QLineEdit('-1.0')
        self.functionHighLabel = QLineEdit('6.0')
        self.optimizerComboBox = QComboBox()
        self.optimizerComboBox.addItems([self.BISECTION, self.GOLDEN_SECTION_SEARCH, self.SCIPY_BISECTION, self.SCIPTY_GOLDEN_SECITION_SEARCH])
        self.runButton = QPushButton('Calculate!')

        # Line edit for iterations and xtol
        self.maxIterationsEdit = QLineEdit('5000')
        self.xtolEdit = QLineEdit('1e-5')

        self.unimodalityCheckPointsEdit = QLineEdit('100')
        self.exhaustiveSerachEdit = QLineEdit('100')

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        # Clean the plot
        self.graphWidget.clear()
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
        self.graphWidget.clear()
        self._plot_function(result)
        self._plot_unimodal_interval(result)
        self._plot_intermediate_intervals(result)
        self._plot_end_interval(result)

    def _plot_function(self, result):
        step = 0.01
        x = np.arange(result.user_interval.low, result.user_interval.high, step)
        y = [result.function.evalute(x) for x in x]

        pen = pg.mkPen(color=(255, 0, 0), width=7, style=QtCore.Qt.DashLine)

        # Plot data: x, y values
        self.graphWidget.plot(x, y, pen=pen)

    def _plot_end_interval(self, result):
        pen = pg.mkPen(width=0)

        # SciPy optimzers do not return the final interval, but only a single point
        if result.minimum_end_interval != None:
            x = [result.minimum_end_interval.low, result.minimum_end_interval.high]
            y = [result.function.evalute(x) for x in x]
            self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

        x = [result.result_x]
        y = [result.function.evalute(result.result_x)]
        self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=40, symbolBrush=('b'))

    def _plot_intermediate_intervals(self, result):
        # The SciPy optimizers does not return the intermediate_intervals
        if result.intermediate_intervals == None:
            return

        x = []
        for interval in result.intermediate_intervals:
            x.append(interval.low)
            x.append(interval.high)
        y = [result.function.evalute(x) for x in x]
        pen = pg.mkPen(width=0)
        self.graphWidget.plot(x, y, pen=pen, symbol='x', symbolSize=15, symbolBrush=('r'))

    def _plot_unimodal_interval(self, result):
        step = 0.01
        x = np.arange(result.unimodal_interval.low, result.unimodal_interval.high, step)
        y = [result.function.evalute(x) for x in x]

        pen = pg.mkPen(color=(30, 240, 0), width=7, style=QtCore.Qt.DashLine)

        # Plot data: x, y values
        self.graphWidget.plot(x, y, pen=pen)

    def _getProgramArguments(self):
        arguments = ProgramArguments()
        arguments.expression = self.functionLabel.text()
        arguments.functionInterval = FunctionInterval(float(self.functionLowPointLabel.text()),
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

        # Max iterations
        arguments.max_iterations = int(self.maxIterationsEdit.text())

        # Xtol
        arguments.xtol = float(self.xtolEdit.text())

        # Unimodality
        arguments.unimodal_check_n = int(self.unimodalityCheckPointsEdit.text())

        # Search
        arguments.exhaustive_serach_n = int(self.exhaustiveSerachEdit.text())

        return arguments
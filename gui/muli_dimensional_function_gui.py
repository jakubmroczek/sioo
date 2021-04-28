import traceback
from PyQt5.QtWidgets import (QLineEdit,
                             QPushButton, QLabel, QMessageBox)
from program_arguments import MuliDimensionProgramArguments
from function import MultiNumberFunction

class MuliDimensionalFunctionGUI:
    DERIVATIVES_LABELS = [
        f'df / d{arg}' for arg in MultiNumberFunction.ARGUMENTS
    ]

    EXAMPLE_FUNCTIONS = {
        2: "x ** 2 + y ** 2",
        3: "x ** 2 + y ** 2 + z ** 2",
        4: "x ** 2 + y ** 2 + z ** 2 + v ** 2",
        5: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2",
        6: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 ",
        7: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 + r ** 2",
        8: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 + r ** 2 + t ** 2",
    }

    def __init__(self, nunmber_of_function_variable):
        self.nunmber_of_function_variable = nunmber_of_function_variable

        self.runButton = QPushButton('Calculate!')

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def add_widgets_to_layout(self, layout, rowIndex):
        '''
        This method is called by the GUI class. The layout object is expected to be of QGridLayout.
        '''
        functionLabel = QLabel('Function:')
        self.function_edit = QLineEdit(self.EXAMPLE_FUNCTIONS[self.nunmber_of_function_variable])

        layout.addWidget(functionLabel, rowIndex + 0, 0, 1, 1)
        layout.addWidget(self.function_edit, rowIndex + 0, 1, 1, 1)

        layout.addWidget(self.runButton, rowIndex + 1, 0, 1, 2)

        derivativeStartRow = rowIndex + 2

        self._add_derivative_widgets_to_layout(layout, derivativeStartRow)

    def _add_derivative_widgets_to_layout(self, layout, startIndex):
        assert self.nunmber_of_function_variable <= len(self.DERIVATIVES_LABELS)

        self.derivative_line_edits = []
        for i in range(len(self.DERIVATIVES_LABELS)):
            label_name = self.DERIVATIVES_LABELS[i]
            label = QLabel(label_name)
            layout.addWidget(label, startIndex, 0, 1, 1)
            line_edit = QLineEdit()
            layout.addWidget(line_edit, startIndex, 1, 1, 1)
            self.derivative_line_edits.append(line_edit)
            startIndex += 1

            if i + 1 > self.nunmber_of_function_variable:
                line_edit.setReadOnly(True)

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
        derivative_expressions = self._get_derivatives_expressions()
        programArugments = MuliDimensionProgramArguments()
        programArugments.derivatives_expressions = derivative_expressions
        return programArugments

    def _get_derivatives_expressions(self):
        expressions = []
        for i in range(self.nunmber_of_function_variable):
            line_edit = self.derivative_line_edits[i]
            expression = line_edit.text()
            expressions.append(expression)
        return expressions
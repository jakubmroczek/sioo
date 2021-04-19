import traceback

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QLabel, QMessageBox, QGridLayout)


class GUI(QDialog):

    MAX_NUMBER_OF_FUNCTION_ARGUMENTS = 8
    NUMBER_OF_BASIC_WIDGETS = 2

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        self.layout = QGridLayout()

        self._add_basic_widgets()

        self.setLayout(self.layout)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _add_basic_widgets(self):
        # Number of function arguments
        functionArgumentLabel = QLabel('Number of functions argument:')
        self.functionArgumentNumberComboBox = QComboBox()
        self.functionArgumentNumberComboBox.addItems([str(x) for x in range(1, self.MAX_NUMBER_OF_FUNCTION_ARGUMENTS
                                                                            + 1)])
        self.functionArgumentNumberComboBox.currentTextChanged.connect(self._on_function_arguments_number_changed)
        self.layout.addWidget(functionArgumentLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.functionArgumentNumberComboBox, 0, 1, 1, 1)

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


    def _on_function_arguments_number_changed(self, value):
        self._remove_extra_widgets()

    def _remove_extra_widgets(self):
        '''
        Removes all the widget except the basic one (function arguments numbr label and combo box).
        '''
        for i in range(self.NUMBER_OF_BASIC_WIDGETS, self.layout.count()):
            self.layout.itemAt(i).widget().setParent(None)


    def _plot(self, result):
        raise Exception('Abstract method called')

    def _getProgramArguments(self):
        raise Exception('Abstract method called')

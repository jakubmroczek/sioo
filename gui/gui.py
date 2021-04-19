from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QLabel, QMessageBox, QGridLayout)
from .one_dimensional_function_gui import OneDimensionalFunctionGUI


class GUI(QDialog):

    MAX_NUMBER_OF_FUNCTION_ARGUMENTS = 8
    NUMBER_OF_BASIC_WIDGETS = 2

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        self.layout = QGridLayout()

        # Tracking current number of function args
        self.is_one_dimensional_function_gui = True

        self._add_basic_widgets()

        self.setLayout(self.layout)

        self.impl = None

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

    def _on_function_arguments_number_changed(self, value):
        if self._should_relayout(value):

            self._remove_extra_widgets()

            if self._should_relayout_to_one_dimenstional():
                self.impl = OneDimensionalFunctionGUI()
                self.impl.add_widgets_to_layout(self.layout, self.NUMBER_OF_BASIC_WIDGETS)
                self.impl.setOnCalculationStart(self.onCalculationStartCallback)
                self.is_one_dimensional_function_gui = True
            else:
                print('multi dim gui')
                self.is_one_dimensional_function_gui = False

    def _remove_extra_widgets(self):
        '''
        Removes all the widget except the basic one (function arguments number label and combo box).
        '''
        for i in reversed(range(self.NUMBER_OF_BASIC_WIDGETS, self.layout.count())):
            if self.layout.itemAt(i):
                self.layout.itemAt(i).widget().setParent(None)


    def _should_relayout(self, value):
        value = int(value)
        single_argument_function_index = 1

        if value > single_argument_function_index:
            return self.is_one_dimensional_function_gui

        if value == single_argument_function_index:
            return not self.is_one_dimensional_function_gui

    def _should_relayout_to_one_dimenstional(self):
        return not self.is_one_dimensional_function_gui

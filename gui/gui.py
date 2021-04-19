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
        self._remove_extra_widgets()
        self.impl = OneDimensionalFunctionGUI()
        self.impl.add_widgets_to_layout(self.layout, self.NUMBER_OF_BASIC_WIDGETS)
        self.impl.setOnCalculationStart(self.onCalculationStartCallback)

    def _remove_extra_widgets(self):
        '''
        Removes all the widget except the basic one (function arguments numbr label and combo box).
        '''
        for i in range(self.NUMBER_OF_BASIC_WIDGETS, self.layout.count()):
            self.layout.itemAt(i).widget().setParent(None)

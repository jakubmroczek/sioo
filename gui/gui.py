from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QLabel, QGridLayout)
from .one_dimensional_function_gui import OneDimensionalFunctionGUI
from .muli_dimensional_function_gui import MuliDimensionalFunctionGUI


class GUI(QDialog):

    MAX_NUMBER_OF_FUNCTION_ARGUMENTS = 8
    NUMBER_OF_BASIC_WIDGETS = 2

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        self.layout = QGridLayout()

        self._add_basic_widgets()

        self.onOneDimensionalCalculationStartCallback = None
        self.onMulitDimensionalCalculationStartCallback = None

        # Tracking current number of function args
        self.is_one_dimensional_function_gui = None
        self.impl = None
        self._init_one_dimensional_function_gui()

        self.setLayout(self.layout)

        self.impl = None

    def setOnOneDimensionalCalculationStart(self, callback):
        self.onOneDimensionalCalculationStartCallback = callback

    def setOnMulitiDimensionalCalcualtionStartCallback(self, callback):
        self.onMulitDimensionalCalculationStartCallback = callback

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

            if self._should_relayout_to_one_dimenstional(value):
                self._init_one_dimensional_function_gui()
            else:
                print('init stuff')
                self._init_multi_dimensional_function_gui()

    def _init_one_dimensional_function_gui(self):
        self.impl = OneDimensionalFunctionGUI()
        self.impl.add_widgets_to_layout(self.layout, self.NUMBER_OF_BASIC_WIDGETS)
        self.impl.setOnCalculationStart(self.onOneDimensionalCalculationStartCallback)
        self.is_one_dimensional_function_gui = True

    def _init_multi_dimensional_function_gui(self):
        function_variables_n = self._get_function_variables_n()
        self.impl = MuliDimensionalFunctionGUI(function_variables_n)
        self.impl.add_widgets_to_layout(self.layout, self.NUMBER_OF_BASIC_WIDGETS)
        self.impl.setOnCalculationStart(self.onMulitDimensionalCalculationStartCallback)
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

        if value == single_argument_function_index:
            return not self.is_one_dimensional_function_gui
        else:
            return True

    def _should_relayout_to_one_dimenstional(self, index):
        index = int(index)
        single_argument_function_index = 1
        print(index)
        print(index == single_argument_function_index)
        return index == single_argument_function_index

    def _get_function_variables_n(self):
        return int(self.functionArgumentNumberComboBox.currentText())

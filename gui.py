from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                             QPushButton)


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        self.functionLabel = QLineEdit('function')
        self.functionRangeLabel = QLineEdit('function range')
        self.optimizerComboBox = QComboBox()
        self.optimizerComboBox.addItems(['Bisection', 'Golden-section search', 'SciPy Bisection', 'Sci-Py Golden-section '
                                                                                             'search'])
        self.runButton = QPushButton('Calculate!')

        layout = QGridLayout()
        layout.addWidget(self.functionLabel, 0, 0, 1, 2)
        layout.addWidget(self.functionRangeLabel, 1, 0, 1, 2)
        layout.addWidget(self.optimizerComboBox, 2, 0, 1, 2)
        layout.addWidget(self.runButton, 3, 0, 1, 2)

        layout.setRowStretch(5, 1)

        self.setLayout(layout)

    def setOnCalculationStart(self, callback):
        self.runButton.clicked.connect(callback)

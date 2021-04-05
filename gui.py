from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        functionLabel = QLineEdit('function')
        functionRangeLabel = QLineEdit('function range')
        optimizerComboBox = QComboBox()
        optimizerComboBox.addItems(['Bisection', 'Golden-section search', 'SciPy Bisection', 'Sci-Py Golden-section '
                                                                                             'search'])
        runButton = QPushButton('Calculate!')

        layout = QGridLayout()
        layout.addWidget(functionLabel, 0, 0, 1, 2)
        layout.addWidget(functionRangeLabel, 1, 0, 1, 2)
        layout.addWidget(optimizerComboBox, 2, 0, 1, 2)
        layout.addWidget(runButton, 3, 0, 1, 2)

        layout.setRowStretch(5, 1)

        self.setLayout(layout)

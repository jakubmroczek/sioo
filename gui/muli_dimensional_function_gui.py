import traceback
from PyQt5.QtWidgets import (QLineEdit,
                             QPushButton, QLabel, QMessageBox)
from pyqtgraph.widgets.ComboBox import ComboBox
from program_arguments import MuliDimensionProgramArguments
from function import MultiNumberFunction
import numpy as np
from gui.plot_3d import Plot3D

class MuliDimensionalFunctionGUI:
    DERIVATIVES_LABELS = [
        f'df / d{arg}' for arg in MultiNumberFunction.ARGUMENTS
    ]

    EXAMPLE_FUNCTIONS = {
        2: "(x - 6) ** 2 + (y - 7) ** 2",
        3: "x ** 2 + y ** 2 + z ** 2",
        4: "x ** 2 + y ** 2 + z ** 2 + v ** 2",
        5: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2",
        6: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 ",
        7: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 + r ** 2",
        8: "x ** 2 + y ** 2 + z ** 2 + v ** 2 + w ** 2 + q ** 2 + r ** 2 + t ** 2",
    }

    EXAMPLE_FUNCTION_X_1 = {
        2: "6, 7",
        3: "1, 2, 3",
        4: "1, 2, 3, 4",
        5: "1, 2, 3, 4, 5",
        6: "1, 2, 3, 4, 5, 6",
        7: "1, 2, 3, 4, 5, 6, 7",
        8: "1, 2, 3, 4, 5, 6, 7, 8",
    }

    EXAMPLE_FUNCTION_DERIVATIVES = [
        '2 * x - 12',
        '2 * y - 14',
        '2 * z',
        '2 * v',
        '2 * w',
        '2 * q',
        '2 * r',
        '2 * t',
    ]

    EXAMPLE_CONSTRAINTS = [
             "-3 * x - 2 * y + 6",
             "-1 * x + y - 3",
             "1 * x + 1 * y - 7",
             " 0.66 * x - y - (4/3)",
    ]
     
    EXAMPLE_CONSTRAINTS_DERIVATIVES = [
        # x derivatives
        '-6 * (-3 * x -2 * y + 6)',
        '-2 * (-1 * x + y - 3)',
        '2 * (x + y - 7)',
        '(4/9) * (2 * x -3 * y - 4)',
        # y derivatives
        '-4 * (-3 * x - 2 * y  + 6)',
        '2 * (-1 * x + y - 3)',
        '2 * (x + y - 7)',
        '(4/3) * -1 * x + 2 * y + (8/3)'
    ]
    
    MAX_NUMBER_OF_CONSTRAINTS = 5

    def __init__(self, nunmber_of_function_variable):
        self.nunmber_of_function_variable = nunmber_of_function_variable
        self.constraints_number = 0

        # Initial position x1
        self.x_1_label = QLabel("Initial position")
        self.x_1_edit = QLineEdit(self.EXAMPLE_FUNCTION_X_1[self.nunmber_of_function_variable])

        # Epsilon
        self.epsilon_label = QLabel("Epsilon")
        self.epsilon_edit = QLineEdit("1e-4")

        # K label
        self.n_label = QLabel("n (max number inner loops)")
        self.n_edit = QLineEdit('10000')

        # Constraints stuff
        self.max_iterations_label = QLabel("SUMT max iterations")
        self.max_iterations_edit = QLineEdit('8')
      
        self.growth_param_label = QLabel("SUMT growth parameters")
        self.growth_param_edit = QLineEdit('2')

        self.c0_label = QLabel("SUMT initial penalty param")
        self.c0_edit = QLineEdit('0.5')

        self.sumt_epsilon_label = QLabel("SUMT epsilon")
        self.sumt_epsilon_edit = QLineEdit('1e-2')

        self.runButton = QPushButton('Calculate!')
        self.runButton.setStyleSheet("background-color: #2958B5")

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

        # Constrained related stuff
        self.constraintsComboBox = ComboBox()
        self.constraintsComboBox.addItems([str(x) for x in range(0, self.MAX_NUMBER_OF_CONSTRAINTS)])
        self.constraintsComboBox.currentTextChanged.connect(self._on_constraints_number_changed)

    def _on_constraints_number_changed(self, value):
        value = int(value)
        old_number = self.constraints_number
        if value != self.constraints_number:
            self.constraints_number = value

        # Delete old stuff
        items_to_delete = old_number + old_number * self.nunmber_of_function_variable
        for i in reversed(range(self.layout.count() - items_to_delete, self.layout.count())):
            if self.layout.itemAt(i):
                self.layout.itemAt(i).widget().setParent(None)

        self.row_index -= items_to_delete

        if self.constraints_number == 0:
            return

        self.row_index = self._add_constraints_widgets_to_layout(self.layout, self.row_index)
        self.row_index = self._add_constraints_derivatives_widgets_to_layout(self.layout, self.row_index)

    def add_widgets_to_layout(self, layout, rowIndex):
        '''
        This method is called by the GUI class. The layout object is expected to be of QGridLayout.
        '''
        functionLabel = QLabel('Function:')
        self.function_edit = QLineEdit(self.EXAMPLE_FUNCTIONS[self.nunmber_of_function_variable])

        layout.addWidget(functionLabel, rowIndex + 0, 0, 1, 1)
        layout.addWidget(self.function_edit, rowIndex + 0, 1, 1, 1)

        layout.addWidget(self.x_1_label, rowIndex + 1, 0, 1, 1)
        layout.addWidget(self.x_1_edit, rowIndex + 1, 1, 1, 1)

        # Epsilon
        layout.addWidget(self.epsilon_label, rowIndex + 2, 0, 1, 1)
        layout.addWidget(self.epsilon_edit, rowIndex + 2, 1, 1, 1)

        # K
        layout.addWidget(self.n_label, rowIndex + 3, 0, 1, 1)
        layout.addWidget(self.n_edit, rowIndex + 3, 1, 1, 1)

        # Constraint stuff
        layout.addWidget(self.max_iterations_label, rowIndex + 4, 0, 1, 1)
        layout.addWidget(self.max_iterations_edit, rowIndex + 4, 1, 1, 1)

        layout.addWidget(self.growth_param_label, rowIndex + 5, 0, 1, 1)
        layout.addWidget(self.growth_param_edit, rowIndex + 5, 1, 1, 1)

        layout.addWidget(self.c0_label, rowIndex + 6, 0, 1, 1)
        layout.addWidget(self.c0_edit, rowIndex + 6, 1, 1, 1)

        layout.addWidget(self.sumt_epsilon_label, rowIndex + 7, 0, 1, 1)
        layout.addWidget(self.sumt_epsilon_edit, rowIndex + 7, 1, 1, 1)

        layout.addWidget(self.runButton, rowIndex + 8, 0, 1, 2)

        derivativeStartRow = rowIndex + 5 + 3 + 1

        rowIndex = self._add_derivative_widgets_to_layout(layout, derivativeStartRow)

        # what should I do here
        label = QLabel("Number of constraints")
        # rowIndex += 1
        layout.addWidget(label, rowIndex, 0, 1, 1)
        # rowIndex += 1
        layout.addWidget(self.constraintsComboBox, rowIndex, 1, 1, 1)

        rowIndex += 1
        rowIndex = self._add_constraints_widgets_to_layout(layout, rowIndex)

        self.row_index = rowIndex
        self.layout = layout

    def _add_derivative_widgets_to_layout(self, layout, startIndex):
        assert self.nunmber_of_function_variable <= len(self.DERIVATIVES_LABELS)

        self.derivative_line_edits = []
        for i in range(len(self.DERIVATIVES_LABELS)):
            label_name = self.DERIVATIVES_LABELS[i]

            label = QLabel(label_name)
            layout.addWidget(label, startIndex, 0, 1, 1)

            derivative_expression = self.EXAMPLE_FUNCTION_DERIVATIVES[i]
            line_edit = QLineEdit()
            if i + 1 <= self.nunmber_of_function_variable:
                line_edit.setText(derivative_expression)
            else:
                line_edit.setReadOnly(True)

            layout.addWidget(line_edit, startIndex, 1, 1, 1)

            self.derivative_line_edits.append(line_edit)

            startIndex += 1

        return startIndex


    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        programArguments = self._getProgramArguments()

        try:
            result = self.onCalculationStartCallback(programArguments)
            #  We only plot if we have 2 dimensional case, otherwise it does not make sense
            if self.nunmber_of_function_variable == 2:
                self._plot(result)
            
            self._print_to_stoudt(result)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            text = f'{str(e)}\n Traceback: "{traceback.print_exc()}"'
            msg.setText(text)
            msg.exec()
        except:
            print(f'Caught unsupported exception!\n Traceback: "{traceback.print_exc()}"')

    def _plot(self, result):
        plot = Plot3D()
        plot.show(result)

    def _print_to_stoudt(self, result):
        print('*' * 100)
        print(f'Function: {result.function.expression}')
        print(f'Minimum at: {result.optimum}')
        print(f'Search history:')
        for index, step in enumerate(result.search_history):
            print(f'\t{index} {step}')
            
        print('')

        if result.log:
            print('')
            print('X_k and c_k')
            for i, log in enumerate(result.log):
                x, c = log
                print(f'{i}. x:{x}, c:{c}')

    def _getProgramArguments(self):
        derivative_expressions = self._get_derivatives_expressions()
        program_arguments = MuliDimensionProgramArguments()
        program_arguments.expression = self._get_function_expression()
        program_arguments.derivatives_expressions = derivative_expressions
        program_arguments.start_x = self._get_start_position()
        program_arguments.argc = self.nunmber_of_function_variable
        program_arguments.epsilon = self._get_epsilon()
        program_arguments.max_iterations = self._get_n()

        if self.constraints_number != 0:
            program_arguments.constraints = self._get_constraints()
            program_arguments.constraints_derivatives = self._get_constrainst_derivatives()

        return program_arguments

    def _get_function_expression(self):
        return self.function_edit.text()

    def _get_derivatives_expressions(self):
        expressions = []
        for i in range(self.nunmber_of_function_variable):
            line_edit = self.derivative_line_edits[i]
            expression = line_edit.text()
            expressions.append(expression)
        return expressions

    def _get_start_position(self):
        expression = self.x_1_edit.text()
        args = expression.split(',')
        args = np.array([float(arg.strip()) for arg in args])
        return args

    def _get_epsilon(self):
        epsilon = float(self.epsilon_edit.text())
        return epsilon

    def _get_n(self):
        k = int(self.n_edit.text())
        return k

    def _get_constraints(self):
        expressions = []
        for line_edit in self.constraints_line_edits:
            expression = line_edit.text()
            expressions.append(expression)
        return expressions

    def _get_constrainst_derivatives(self):
        expressions = []
        for line_edit in self.constraints_derivatives_edits:
            expression = line_edit.text()
            expressions.append(expression)
        return expressions

    def _add_constraints_widgets_to_layout(self, layout, startIndex):
            assert self.constraints_number < self.MAX_NUMBER_OF_CONSTRAINTS

            if self.constraints_number == 0:
                return startIndex

            self.constraints_line_edits = []
            for i in range(self.constraints_number):
                label_name = f'Constraint {i + 1}'

                label = QLabel(label_name)
                layout.addWidget(label, startIndex, 0, 1, 1)

                expression = self.EXAMPLE_CONSTRAINTS[i]
                line_edit = QLineEdit()
       
                if i + 1 <= self.constraints_number:
                    line_edit.setText(expression)
                else:
                    line_edit.setReadOnly(True)

                layout.addWidget(line_edit, startIndex, 1, 1, 1)

                self.constraints_line_edits.append(line_edit)

                startIndex += 1

            return startIndex

    def _add_constraints_derivatives_widgets_to_layout(self, layout, row_index):
            startIndex = row_index
            
            if self.constraints_number == 0:
                return startIndex

            self.constraints_derivatives_edits = []

            for i in range(self.nunmber_of_function_variable):
                variable = MultiNumberFunction.ARGUMENTS[i]

                for j in range(self.constraints_number):
                    label_name = f'Constraint {j + 1} derivative df \ d{variable}'
                    label = QLabel(label_name)
                    layout.addWidget(label, startIndex, 0, 1, 1)

                    #  we have 4 per x, y in examples
                    index = i * 4 + j
                    expression = ''
                   
                    # Examples only for first 2 variables
                    if i >= 2:
                        expression = '0'
                    else:
                        expression = self.EXAMPLE_CONSTRAINTS_DERIVATIVES[index] 

                    line_edit = QLineEdit()
                    line_edit.setText(expression)
                    layout.addWidget(line_edit, startIndex, 1, 1, 1)
                    self.constraints_derivatives_edits.append(line_edit)
                    
                    startIndex += 1
            
            return startIndex

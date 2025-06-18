import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Calculator")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Display Widgets ---
        self.operand1_display = QLineEdit()
        self.operand1_display.setReadOnly(True)
        self.operand1_display.setAlignment(Qt.AlignRight)
        self.operand1_display.setStyleSheet("font-size: 24pt; padding: 5px;")

        self.operator_display = QLineEdit()
        self.operator_display.setReadOnly(True)
        self.operator_display.setAlignment(Qt.AlignCenter)
        self.operator_display.setStyleSheet("font-size: 18pt; padding: 2px; color: orange;")

        self.operand2_display = QLineEdit()
        self.operand2_display.setReadOnly(True)
        self.operand2_display.setAlignment(Qt.AlignRight)
        self.operand2_display.setStyleSheet("font-size: 24pt; padding: 5px;")

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setStyleSheet("font-size: 36pt; padding: 10px; background-color: #e0ffe0; color: green;")

        # Layout for displays
        display_layout = QHBoxLayout()
        display_layout.addWidget(self.operand1_display)
        display_layout.addWidget(self.operator_display)
        display_layout.addWidget(self.operand2_display)

        self.main_layout.addLayout(display_layout)
        self.main_layout.addWidget(self.result_display) # Result display on its own row

        # --- Buttons ---
        self.buttons_layout = QGridLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.create_buttons()
        self.clear_all() # Initialize display and internal state

    def create_buttons(self):
        buttons = [
            ('C', 0, 0, 1, 1, self.clear_all, 'clear'),
            ('7', 1, 0, 1, 1, lambda: self.number_pressed('7'), 'number'),
            ('8', 1, 1, 1, 1, lambda: self.number_pressed('8'), 'number'),
            ('9', 1, 2, 1, 1, lambda: self.number_pressed('9'), 'number'),
            ('/', 1, 3, 1, 1, lambda: self.operator_pressed('/'), 'operator'),

            ('4', 2, 0, 1, 1, lambda: self.number_pressed('4'), 'number'),
            ('5', 2, 1, 1, 1, lambda: self.number_pressed('5'), 'number'),
            ('6', 2, 2, 1, 1, lambda: self.number_pressed('6'), 'number'),
            ('*', 2, 3, 1, 1, lambda: self.operator_pressed('*'), 'operator'),

            ('1', 3, 0, 1, 1, lambda: self.number_pressed('1'), 'number'),
            ('2', 3, 1, 1, 1, lambda: self.number_pressed('2'), 'number'),
            ('3', 3, 2, 1, 1, lambda: self.number_pressed('3'), 'number'),
            ('-', 3, 3, 1, 1, lambda: self.operator_pressed('-'), 'operator'),

            ('0', 4, 0, 1, 1, lambda: self.number_pressed('0'), 'number'),
            ('.', 4, 1, 1, 1, lambda: self.number_pressed('.'), 'decimal'),
            ('=', 4, 2, 1, 2, self.equals_pressed, 'equals'), # Span 2 columns
            ('+', 5, 3, 1, 1, lambda: self.operator_pressed('+'), 'operator'), # Corrected row for +
        ]

        # Dynamically add buttons to grid
        for btn_text, row, col, row_span, col_span, callback, style_class in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(callback)
            button.setFixedSize(60, 60) # Example fixed size
            button.setStyleSheet(f"font-size: 16pt; background-color: {'#d9534f' if style_class == 'clear' else '#5cb85c' if style_class == 'equals' else '#f0ad4e' if style_class == 'operator' else '#666666'}; color: white; border-radius: 5px;")
            self.buttons_layout.addWidget(button, row, col, row_span, col_span)


    # --- Internal State Variables ---
    current_operand = 1 # 1 for operand1, 2 for operand2
    operand1_val = ""
    operand2_val = ""
    operator_val = ""
    awaiting_new_operand2 = False # Flag to manage operand2 input after operator

    def number_pressed(self, digit):
        if self.awaiting_new_operand2:
            self.operand2_val = "" # Clear operand2 for new input
            self.awaiting_new_operand2 = False

        if self.operator_val == "": # Still building operand1
            if digit == '.' and '.' in self.operand1_val:
                return # Prevent multiple decimals
            self.operand1_val += digit
            self.operand1_display.setText(self.operand1_val)
        else: # Building operand2
            if digit == '.' and '.' in self.operand2_val:
                return # Prevent multiple decimals
            self.operand2_val += digit
            self.operand2_display.setText(self.operand2_val)

    def operator_pressed(self, op):
        if self.operand1_val == "":
            self.operand1_val = "0" # Default to 0 if no number entered yet

        if self.operator_val != "" and self.operand2_val != "":
            # If an operator is already set and operand2 is present, calculate intermediate result
            self.calculate_result()
            self.operand1_val = self.result_display.text() # Result becomes new operand1
            self.operand1_display.setText(self.operand1_val)
            self.operand2_val = "" # Clear operand2 for the next operation
            self.result_display.setText("") # Clear result for new operation

        self.operator_val = op
        self.operator_display.setText(self.operator_val)
        self.operand2_display.setText("") # FIX 1: operand2_display should be empty
        self.awaiting_new_operand2 = True # Ready for new operand2 input

    def equals_pressed(self):
        self.calculate_result()

    def calculate_result(self):
        if self.operator_val == "" or self.operand1_val == "" or self.operand2_val == "":
            return # Cannot calculate if incomplete

        try:
            num1 = float(self.operand1_val)
            num2 = float(self.operand2_val)
            result = 0

            if self.operator_val == '+':
                result = num1 + num2
            elif self.operator_val == '-':
                result = num1 - num2
            elif self.operator_val == '*':
                result = num1 * num2
            elif self.operator_val == '/':
                if num2 == 0:
                    self.result_display.setText("Error: Div by 0")
                    self.clear_state_on_error()
                    return
                result = num1 / num2
            # Add more operators as needed

            self.result_display.setText(str(result)) # FIX 2: Result ONLY in result_display
            # FIX 3: operand2_display remains unchanged (it already has operand2_val)
            # No need to explicitly set operand2_display.setText(self.operand2_val) here
            # because it was already set by number_pressed and not overwritten.

            # Prepare for next operation (result becomes operand1)
            self.operand1_val = str(result)
            self.operator_val = ""
            self.operator_display.setText("")
            self.awaiting_new_operand2 = True # Ready for a new operand2 if chaining

        except ValueError:
            self.result_display.setText("Error")
            self.clear_state_on_error()
        except Exception as e:
            self.result_display.setText(f"Error: {e}")
            self.clear_state_on_error()

    def clear_all(self):
        self.operand1_val = ""
        self.operand2_val = ""
        self.operator_val = ""
        self.awaiting_new_operand2 = False

        self.operand1_display.setText("")
        self.operator_display.setText("")
        self.operand2_display.setText("")
        self.result_display.setText("")

    def clear_state_on_error(self):
        # Clear internal state but keep current display for context (e.g., error message)
        self.operand1_val = ""
        self.operand2_val = ""
        self.operator_val = ""
        self.awaiting_new_operand2 = False
        self.operator_display.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
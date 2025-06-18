import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QButtonGroup, QLabel
)
from PySide6.QtCore import Qt

class CalculatorLogic:
    """Handles the core logic of the calculator, independent of the GUI."""
    def __init__(self):
        self.current_number = 0
        self.previous_number = 0
        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = False

        self.base_mode = "dec"
        self.bit_width = 16
        self.signed_mode = True

    def _apply_bit_width_and_sign(self, num):
        mask = (1 << self.bit_width) - 1
        num_masked = num & mask

        if self.signed_mode:
            msb_mask = 1 << (self.bit_width - 1)
            if (num_masked & msb_mask) and self.bit_width > 0:
                return num_masked - (1 << self.bit_width)
        return num_masked

    def _validate_input_string_to_int(self, num_str):
        try:
            if self.base_mode == "bin":
                return int(num_str, 2)
            elif self.base_mode == "hex":
                return int(num_str, 16)
            else:
                return int(num_str)
        except ValueError:
            return 0

    def get_display_value(self, num=None):
        if num is None:
            num = self.current_number
        num = self._apply_bit_width_and_sign(num)

        if self.base_mode == "bin":
            formatted_num = bin(num & ((1 << self.bit_width) - 1))[2:].zfill(self.bit_width)
        elif self.base_mode == "hex":
            hex_chars = self.bit_width // 4
            formatted_num = hex(num & ((1 << self.bit_width) - 1))[2:].upper().zfill(hex_chars)
        else:
            formatted_num = str(num)
        return formatted_num

    def press_number(self, digit):
        if self.new_number_started:
            self.current_number = 0
            self.new_number_started = False

        current_display_str = self.get_display_value()
        new_num_str = current_display_str + digit
        self.current_number = self._validate_input_string_to_int(new_num_str)

    def press_clear(self):
        self.current_number = 0
        self.previous_number = 0
        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = False

    def press_two_operand_operation(self, op_type):
        self.previous_number = self.current_number
        self.operation = op_type
        self.waiting_for_second_operand = True
        self.new_number_started = True

    def press_equals(self):
        if not self.waiting_for_second_operand or self.operation is None:
            return "ERROR"

        num1 = self._apply_bit_width_and_sign(self.previous_number)
        num2 = self._apply_bit_width_and_sign(self.current_number)

        try:
            if self.operation == "add":
                result = num1 + num2
            elif self.operation == "subtract":
                result = num1 - num2
            else:
                result = 0

            self.current_number = self._apply_bit_width_and_sign(result)
            self.operation = None
            self.waiting_for_second_operand = False

        except Exception:
            self.current_number = 0

        return self.get_display_value()

class CalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Calculator")

        self.calculator_logic = CalculatorLogic()

        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self.main_layout = QVBoxLayout(self._central_widget)

        self._create_displays()
        self._create_buttons()

    def _create_displays(self):
        self.operand1_display = QLineEdit("0")
        self.operand1_display.setReadOnly(True)
        self.operand1_display.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.operand1_display)

        self.operand2_display = QLineEdit()
        self.operand2_display.setReadOnly(True)
        self.operand2_display.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.operand2_display)

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.main_layout.addWidget(self.result_display)

    def _create_buttons(self):
        buttons_layout = QGridLayout()

        buttons = [
            ('C', 0, 0), ('+', 0, 1), ('-', 0, 2), ('=', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 4, 1)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda checked, t=text: self._on_button_pressed(t))
            buttons_layout.addWidget(button, row, col)

        self.main_layout.addLayout(buttons_layout)

    def _on_button_pressed(self, button_text):
        if button_text.isdigit():
            self.calculator_logic.press_number(button_text)
            self.operand2_display.setText(self.calculator_logic.get_display_value())
        elif button_text in ['+', '-']:
            self.calculator_logic.press_two_operand_operation(button_text)
            self.operand1_display.setText(self.calculator_logic.get_display_value(self.calculator_logic.previous_number))
            self.operand2_display.clear()
        elif button_text == '=':
            result = self.calculator_logic.press_equals()
            self.result_display.setText(result)
            self.operand2_display.setText(self.calculator_logic.get_display_value())  # Keep operand2 displayed
        elif button_text == 'C':
            self.calculator_logic.press_clear()
            self.operand1_display.setText("0")
            self.operand2_display.clear()
            self.result_display.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorGUI()
    window.show()
    sys.exit(app.exec())

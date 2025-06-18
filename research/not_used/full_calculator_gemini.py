import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QButtonGroup, QLabel # Added QLabel for mode titles for better accessibility/standard practice
)
from PySide6.QtCore import Qt

class CalculatorLogic:
    """
    Handles the core logic of the calculator, independent of the GUI.
    """
    def __init__(self):
        self.current_number = 0
        self.previous_number = 0
        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = False

        self.base_mode = "dec"
        self.bit_width = 32
        self.signed_mode = True

    def _apply_bit_width_and_sign(self, num):
        mask = (1 << self.bit_width) - 1
        num_masked = num & mask

        if self.signed_mode:
            msb_mask = 1 << (self.bit_width - 1)
            # Ensure bit_width > 0 to prevent issues with 1 << 0 (e.g., if bit_width was mistakenly 0)
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
            print(f"Invalid input for base {self.base_mode}: '{num_str}'", file=sys.stderr)
            return 0

    def get_display_value(self):
        try:
            num = self._apply_bit_width_and_sign(self.current_number)

            if self.base_mode == "bin":
                formatted_num = bin(num & ((1 << self.bit_width) - 1))[2:].zfill(self.bit_width)
            elif self.base_mode == "hex":
                hex_chars = (self.bit_width + 3) // 4
                formatted_num = hex(num & ((1 << self.bit_width) - 1))[2:].upper().zfill(hex_chars)
            else:
                formatted_num = str(num)
            return formatted_num
        except Exception as e:
            print(f"Error getting display value: {e}", file=sys.stderr)
            return "ERROR"

    def press_number(self, digit):
        current_display_str = self.get_display_value()

        if self.new_number_started:
            current_display_str = "0"
            self.new_number_started = False
            self.current_number = 0

        if current_display_str == "0" and digit == "0":
            return

        valid_digits = {
            "bin": "01",
            "dec": "0123456789",
            "hex": "0123456789ABCDEFabcdef"
        }
        if digit.upper() not in valid_digits[self.base_mode]:
            return

        if current_display_str == "0":
            new_num_str = digit
        else:
            new_num_str = current_display_str + digit

        # Prevent input string from becoming excessively long (e.g., 64 chars for 32-bit bin)
        # This is a heuristic to prevent ValueError on int(long_string, 2)
        max_len = self.bit_width if self.base_mode == "bin" else \
                  (self.bit_width + 3) // 4 if self.base_mode == "hex" else \
                  12 # Arbitrary max length for decimal to prevent absurdly long numbers

        if len(new_num_str) > max_len and new_num_str != "0": # Allow '0' to be typed initially
             return

        self.current_number = self._validate_input_string_to_int(new_num_str)

    def press_clear(self):
        self.current_number = 0
        self.previous_number = 0
        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = False

    def set_base_mode(self, mode):
        if mode in ["bin", "dec", "hex"]:
            self.base_mode = mode
        else:
            print(f"Invalid base mode: {mode}", file=sys.stderr)

    def set_bit_width(self, width):
        if width in [8, 16, 32]:
            self.bit_width = width
        else:
            print(f"Invalid bit width: {width}", file=sys.stderr)

    def set_signed_mode(self, signed):
        self.signed_mode = signed

    def press_one_operand_operation(self, op_type):
        num = self._apply_bit_width_and_sign(self.current_number)
        result = 0

        try:
            if op_type == "not":
                result = (~num) & ((1 << self.bit_width) - 1)
            elif op_type == "shl":
                result = (num << 1) & ((1 << self.bit_width) - 1)
            elif op_type == "shr":
                if self.signed_mode:
                    result = num >> 1
                else:
                    result = (num % (1 << self.bit_width)) >> 1
            else:
                print(f"Unknown one-operand operation: {op_type}", file=sys.stderr)
                return

            self.current_number = result
        except Exception as e:
            print(f"Error during one-operand operation {op_type}: {e}", file=sys.stderr)
            self.current_number = 0

        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = True

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
        result = 0
        error_state = False

        try:
            if self.operation == "add":
                result = num1 + num2
            elif self.operation == "subtract":
                result = num1 - num2
            elif self.operation == "multiply":
                result = num1 * num2
            elif self.operation == "divide":
                if num2 == 0:
                    self.current_number = 0
                    self.previous_number = 0
                    self.operation = None
                    self.waiting_for_second_operand = False
                    self.new_number_started = True
                    return "DIV BY ZERO"
                result = num1 // num2
            elif self.operation == "and":
                result = num1 & num2
            elif self.operation == "or":
                result = num1 | num2
            elif self.operation == "xor":
                result = num1 ^ num2
            else:
                print(f"Unknown two-operand operation: {self.operation}", file=sys.stderr)
                error_state = True

            self.current_number = self._apply_bit_width_and_sign(result)

        except Exception as e:
            print(f"Calculation error: {e}", file=sys.stderr)
            error_state = True
            self.current_number = 0

        self.operation = None
        self.waiting_for_second_operand = False
        self.new_number_started = True

        return self.get_display_value() if not error_state else "ERROR"


class CalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Calculator")
        self.setGeometry(100, 100, 450, 600)

        self.calculator_logic = CalculatorLogic()

        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self.main_layout = QVBoxLayout(self._central_widget)

        # Store references to hex digit buttons
        self.hex_digit_buttons = {}

        self._create_display()
        self._create_mode_controls()
        self._create_buttons() # Buttons creation now populates self.hex_digit_buttons
        self._update_display()
        self._update_hex_button_state() # Call after all buttons are created

    def _create_display(self):
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(60)
        font = self.display.font()
        font.setPointSize(24)
        self.display.setFont(font)
        self.main_layout.addWidget(self.display)

    def _create_mode_controls(self):
        modes_layout = QHBoxLayout()

        # Base Mode Buttons
        base_group_layout = QVBoxLayout()
        # Use QLabel for titles for better standard practice
        base_group_layout.addWidget(QLabel("Base:"))
        self.base_group = QButtonGroup(self)
        for mode in ["Dec", "Hex", "Bin"]:
            btn = QPushButton(mode)
            btn.setCheckable(True)
            self.base_group.addButton(btn)
            base_group_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, m=mode.lower(): self._set_base_mode(m))
            if mode == "Dec":
                btn.setChecked(True)
        modes_layout.addLayout(base_group_layout)

        # Bit Width Buttons
        bit_width_group_layout = QVBoxLayout()
        bit_width_group_layout.addWidget(QLabel("Bits:"))
        self.bit_width_group = QButtonGroup(self)
        for width in [8, 16, 32]:
            btn = QPushButton(f"{width}-bit")
            btn.setCheckable(True)
            self.bit_width_group.addButton(btn)
            bit_width_group_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, w=width: self._set_bit_width(w))
            if width == 32:
                btn.setChecked(True)
        modes_layout.addLayout(bit_width_group_layout)

        # Signed/Unsigned Buttons
        signed_mode_group_layout = QVBoxLayout()
        signed_mode_group_layout.addWidget(QLabel("Sign:"))
        self.signed_mode_group = QButtonGroup(self)
        for text, signed in [("Signed", True), ("Unsigned", False)]:
            btn = QPushButton(text)
            btn.setCheckable(True)
            self.signed_mode_group.addButton(btn)
            signed_mode_group_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, s=signed: self._set_signed_mode(s))
            if signed:
                btn.setChecked(True)
        modes_layout.addLayout(signed_mode_group_layout)

        self.main_layout.addLayout(modes_layout)

    def _create_buttons(self):
        buttons_layout = QGridLayout()

        buttons_data = [
            ("C", 0, 0, 'clear'), ("<<", 0, 1, 'one_op'), (">>", 0, 2, 'one_op'), ("NOT", 0, 3, 'one_op'),
            ("A", 1, 0, 'digit'), ("B", 1, 1, 'digit'), ("C", 1, 2, 'digit'), ("/", 1, 3, 'two_op'),
            ("D", 2, 0, 'digit'), ("E", 2, 1, 'digit'), ("F", 2, 2, 'digit'), ("*", 2, 3, 'two_op'),
            ("7", 3, 0, 'digit'), ("8", 3, 1, 'digit'), ("9", 3, 2, 'digit'), ("-", 3, 3, 'two_op'),
            ("4", 4, 0, 'digit'), ("5", 4, 1, 'digit'), ("6", 4, 2, 'digit'), ("+", 4, 3, 'two_op'),
            ("1", 5, 0, 'digit'), ("2", 5, 1, 'digit'), ("3", 5, 2, 'digit'), ("AND", 5, 3, 'two_op'),
            ("0", 6, 0, 'digit'), ("OR", 6, 1, 'two_op'), ("XOR", 6, 2, 'two_op'), ("=", 6, 3, 'equals'),
        ]

        op_map = {
            "+": "add", "-": "subtract", "*": "multiply", "/": "divide",
            "AND": "and", "OR": "or", "XOR": "xor",
            "<<": "shl", ">>": "shr", "NOT": "not"
        }

        for btn_text, row, col, btn_type in buttons_data:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)

            if btn_type == 'digit':
                button.clicked.connect(lambda checked, text=btn_text: self._handle_digit_press(text))
                if btn_text in "ABCDEF":
                    self.hex_digit_buttons[btn_text] = button # Store reference to hex buttons
            elif btn_type == 'two_op':
                button.clicked.connect(lambda checked, op=op_map[btn_text]: self._handle_two_operand_op(op))
            elif btn_type == 'one_op':
                button.clicked.connect(lambda checked, op=op_map[btn_text]: self._handle_one_operand_op(op))
            elif btn_type == 'equals':
                button.clicked.connect(self._handle_equals_press)
            elif btn_type == 'clear':
                button.clicked.connect(self._handle_clear_press)

            buttons_layout.addWidget(button, row, col) # No row_span/col_span in data, assume 1x1

        self.main_layout.addLayout(buttons_layout)

    # Replaced _create_label with direct QLabel usage where appropriate
    # def _create_label(self, text):
    #     label = QLineEdit(text)
    #     label.setReadOnly(True)
    #     label.setAlignment(Qt.AlignCenter)
    #     label.setStyleSheet("border: none; background-color: transparent; color: #555;")
    #     return label

    # --- GUI Event Handlers ---

    def _update_display(self):
        self.display.setText(self.calculator_logic.get_display_value())

    def _handle_digit_press(self, digit):
        self.calculator_logic.press_number(digit)
        self._update_display()
        # No need to call _update_hex_button_state here, as base mode isn't changed by digit press

    def _handle_one_operand_op(self, op_type):
        self.calculator_logic.press_one_operand_operation(op_type)
        self._update_display()

    def _handle_two_operand_op(self, op_type):
        self.calculator_logic.press_two_operand_operation(op_type)
        self._update_display()

    def _handle_equals_press(self):
        result = self.calculator_logic.press_equals()
        self.display.setText(result)

    def _handle_clear_press(self):
        self.calculator_logic.press_clear()
        self._update_display()
        self._update_hex_button_state() # Ensure hex buttons are enabled/disabled correctly

    def _set_base_mode(self, mode):
        self.calculator_logic.set_base_mode(mode)
        self._update_display()
        self._update_hex_button_state() # Crucial: call when base mode changes

    def _set_bit_width(self, width):
        self.calculator_logic.set_bit_width(width)
        self._update_display()

    def _set_signed_mode(self, signed):
        self.calculator_logic.set_signed_mode(signed)
        self._update_display()

    def _update_hex_button_state(self):
        """Enables/disables A-F buttons based on the current base mode."""
        is_hex_mode = (self.calculator_logic.base_mode == "hex")
        for btn_text, button in self.hex_digit_buttons.items():
            button.setEnabled(is_hex_mode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorGUI()
    window.show()
    sys.exit(app.exec())
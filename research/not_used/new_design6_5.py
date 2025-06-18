# As of 2025-04-15 at noon, this version is exactly the same as new_design6_4.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGridLayout, QPushButton, QButtonGroup, QRadioButton
)
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

class BaseConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.clear_input = False # controls when clicking a digit button clears the input
        self.setWindowTitle("C-64 Programmer's Calculator")

        self.current_input_mode = "dec"
        self.first_operand = None # No longer used in the same way
        self.current_operation = None # No longer used in the same way
        self.current_bit_width = 16  # Default bit width

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)

        self.hex_label = QLabel("$0")
        self.dec_label = QLabel("0")
        self.bin_label = QLabel("%0")
        self.twos_complement_label = QLabel("2's: 0")
        self.error_label = QLabel("") # For error messages

        # Mode Selection Buttons
        self.hex_mode_button = QPushButton("Hex")
        self.dec_mode_button = QPushButton("Dec")
        self.bin_mode_button = QPushButton("Bin")

        self.hex_mode_button.setCheckable(True)
        self.dec_mode_button.setCheckable(True)
        self.bin_mode_button.setCheckable(True)

        self.dec_mode_button.setChecked(True) # Set initial checked state

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.hex_mode_button)
        self.mode_group.addButton(self.dec_mode_button)
        self.mode_group.addButton(self.bin_mode_button)

        self.hex_mode_button.clicked.connect(self.set_input_mode)
        self.dec_mode_button.clicked.connect(self.set_input_mode)
        self.bin_mode_button.clicked.connect(self.set_input_mode)

        # Bit Width Selection Buttons
        self.bit_width_8 = QPushButton("8-bit")
        self.bit_width_16 = QPushButton("16-bit")
        self.bit_width_32 = QPushButton("32-bit")

        self.bit_width_8.setCheckable(True)
        self.bit_width_16.setCheckable(True)
        self.bit_width_32.setCheckable(True)

        self.bit_width_16.setChecked(True)  # Default to 16-bit

        self.bit_width_group = QButtonGroup()
        self.bit_width_group.addButton(self.bit_width_8)
        self.bit_width_group.addButton(self.bit_width_16)
        self.bit_width_group.addButton(self.bit_width_32)

        # Operation Buttons
        self.add_button = QPushButton("+")
        self.subtract_button = QPushButton("-")
        self.multiply_button = QPushButton("*")
        self.divide_button = QPushButton("/")
        self.and_button = QPushButton("AND")
        self.or_button = QPushButton("OR")
        self.xor_button = QPushButton("XOR")
        self.shift_left_button = QPushButton("<<")
        self.shift_right_button = QPushButton(">>")
        self.not_button = QPushButton("NOT")
        self.equals_button = QPushButton("=")
        self.clear_button = QPushButton("Clear")
        self.backspace_button = QPushButton("Backspace")

        # Connect Operation Buttons
        self.bit_width_8.clicked.connect(lambda: self.set_bit_width(8))
        self.bit_width_16.clicked.connect(lambda: self.set_bit_width(16))
        self.bit_width_32.clicked.connect(lambda: self.set_bit_width(32))
        self.add_button.clicked.connect(self.add_clicked)
        self.subtract_button.clicked.connect(self.subtract_clicked)
        self.multiply_button.clicked.connect(self.multiply_clicked)
        self.divide_button.clicked.connect(self.divide_clicked)
        self.and_button.clicked.connect(self.and_clicked)
        self.or_button.clicked.connect(self.or_clicked)
        self.xor_button.clicked.connect(self.xor_clicked)
        self.shift_left_button.clicked.connect(self.perform_shift_left)
        self.shift_right_button.clicked.connect(self.perform_shift_right)
        self.not_button.clicked.connect(self.perform_not)
        self.equals_button.clicked.connect(self.perform_equals)
        self.clear_button.clicked.connect(self.clear_all)
        self.backspace_button.clicked.connect(self.backspace_clicked)

        # Ensure only one bit width button is checked at a time
        self.bit_width_group.buttonClicked.connect(self.update_bit_width_checked)

        # Buttons Layout (Digits and Hex)
        buttons_layout = QGridLayout()
        buttons = [
            "D", "E", "F",
            "A", "B", "C",
            "7", "8", "9",  # Corrected order
            "4", "5", "6",  # Corrected order
            "1", "2", "3",  # Corrected order
            "(", ".", ")"
        ]

        row, col = 0, 0
        for button_name in buttons:
            button = QPushButton(button_name)
            button.clicked.connect(lambda checked, label = button_name: self.handle_input(label))
            buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        zero_button = QPushButton("0")
        zero_button.clicked.connect(lambda checked, label = "0": self.handle_input(label))
        buttons_layout.addWidget(zero_button, 5, 1) # '0' on its own row (index 5), centered

        # Operation Buttons Layout (Grid)
        operators_layout = QGridLayout()
        operators = [
            self.add_button, self.subtract_button, self.multiply_button, self.divide_button,
            self.and_button, self.or_button, self.xor_button, self.not_button,
            self.shift_left_button, self.shift_right_button, self.clear_button, self.backspace_button
        ]
        row, col = 0, 0
        for button in operators:
            operators_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Equals Button Layout (Full Width)
        equals_layout = QHBoxLayout()
        equals_layout.addWidget(self.equals_button)

        # Mode Selection Layout (Horizontal)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.hex_mode_button)
        mode_layout.addWidget(self.dec_mode_button)
        mode_layout.addWidget(self.bin_mode_button)

        # Bit Width Selection Layout (Horizontal)
        bit_width_layout = QHBoxLayout()
        bit_width_layout.addWidget(self.bit_width_8)
        bit_width_layout.addWidget(self.bit_width_16)
        bit_width_layout.addWidget(self.bit_width_32)

        # Labels Layout (Grid)
        labels_layout = QGridLayout()
        labels_layout.addWidget(self.hex_label, 0, 0)
        labels_layout.addWidget(self.dec_label, 0, 1)
        labels_layout.addWidget(self.bin_label, 1, 0)
        labels_layout.addWidget(self.twos_complement_label, 1, 1)

        # Main Layout (Vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(bit_width_layout)
        main_layout.addLayout(buttons_layout) # The digit/hex grid
        main_layout.addLayout(operators_layout) # The operator grid
        main_layout.addLayout(equals_layout) # Full-width equals button
        main_layout.addWidget(self.error_label) # Error message label

        self.setLayout(main_layout)

        # Center the window on the primary screen
        screen = QApplication.primaryScreen()

        if screen:
            screen_geometry = screen.geometry()
            window_geometry = self.frameGeometry()
            x = screen_geometry.x() + (screen_geometry.width() - window_geometry.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - window_geometry.height()) // 2
            self.move(x, y)
        else:
            self.setGeometry(100, 100, 400, 300)

        self.set_input_mode() # Set initial validator

    def add_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} + ")

    def subtract_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} - ")

    def multiply_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} * ")

    def divide_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} / ")

    def and_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} AND ")

    def or_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} OR ")

    def xor_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} XOR ")

    def shift_left_clicked(self): # Renamed to match button connection
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} << ")

    def shift_right_clicked(self): # Renamed to match button connection
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} >> ")

    def backspace_clicked(self):
        current_text = self.input_field.text()
        self.input_field.setText(current_text[:-1]) # Remove the last character
        self.update_labels(self.input_field.text())
        
    def update_bit_width_checked(self, button):
        for btn in self.bit_width_group.buttons():
            if btn != button:
                btn.setChecked(False)
        self.current_bit_width = int(button.text().split('-')[0])
        self.update_labels(self.input_field.text())

    def set_bit_width(self, width):
        self.current_bit_width = width
        for button in self.bit_width_group.buttons():
            if button.text().startswith(f"{width}-bit"):
                button.setChecked(True)
            else:
                button.setChecked(False)
        self.update_labels(self.input_field.text())

    def add_clicked(self):
        self.operation_clicked("+")
        
    def set_default_mode(self):
        self.dec_mode_button.setChecked(True)
        self.set_input_mode()

    def set_input_mode(self):
        checked_button = None
        for button in self.mode_group.buttons():
            if button.isChecked():
                checked_button = button
                break

        if checked_button:
            previous_mode = self.current_input_mode
            self.current_input_mode = checked_button.text().lower()
            current_text = self.input_field.text()

            if current_text:
                try:
                    if previous_mode == "hex":
                        decimal_value = int(current_text, 16)
                    elif previous_mode == "bin":
                        decimal_value = int(current_text, 2)
                    else:  # decimal
                        decimal_value = int(current_text)

                    if self.current_input_mode == "hex":
                        new_text = hex(decimal_value)[2:].upper()
                        self.input_field.setText(new_text)
                    elif self.current_input_mode == "bin":
                        new_text = bin(decimal_value)[2:]
                        self.input_field.setText(new_text)
                    else:  # decimal
                        new_text = str(decimal_value)
                        self.input_field.setText(new_text)

                except ValueError:
                    self.input_field.setText("Error")
                    self.update_labels("Error") # Update labels on error
                finally:
                    # Explicitly update labels after (attempted) conversion
                    self.update_labels(self.input_field.text())
            else:
                # If the input field is empty, just update labels with empty string
                self.update_labels("")

            # Set the validator for the new mode
            validator = None
            if self.current_input_mode == "hex":
                regex = QRegularExpression("[0-9a-fA-F]*")
                validator = QRegularExpressionValidator(regex)
            elif self.current_input_mode == "bin":
                regex = QRegularExpression("[01]*")
                validator = QRegularExpressionValidator(regex)
            else:  # decimal
                validator = QIntValidator()
            self.input_field.setValidator(validator)

    def update_labels(self, value):
        if isinstance(value, str) and value == "Error":
            self.hex_label.setText("$Error")
            self.dec_label.setText("Error")
            self.bin_label.setText("%Error")
            self.twos_complement_label.setText("2's: Error")
            return

        masked_decimal = 0  # Default value
        grouped_hex = ""  # Initialize grouped_hex here
        grouped_bin = ""  # Initialize grouped_bin here

        try:
            if self.current_input_mode == "hex" and value:
                decimal_value = int(value, 16)
                masked_decimal = decimal_value & ((1 << self.current_bit_width) - 1)
            elif self.current_input_mode == "bin" and value:
                decimal_value = int(value, 2)
                masked_decimal = decimal_value & ((1 << self.current_bit_width) - 1)
            elif value:
                decimal_value = int(value)
                masked_decimal = decimal_value & ((1 << self.current_bit_width) - 1)
            elif not value:  # Handle empty input
                pass # Keep masked_decimal as 0

            hex_value = hex(masked_decimal)[2:].upper().zfill(self.current_bit_width // 4)
            dec_value = str(masked_decimal)
            bin_value = bin(masked_decimal)[2:].zfill(self.current_bit_width)

            # Calculate two's complement (as signed decimal and binary if negative)
            if (masked_decimal >> (self.current_bit_width - 1)) & 1: # Check if MSB is 1
                signed_decimal = masked_decimal - (1 << self.current_bit_width)
                twos_complement_bin = bin(signed_decimal & ((1 << self.current_bit_width) - 1))[2:].zfill(self.current_bit_width)
                self.twos_complement_label.setText(f"2's: {signed_decimal} ({twos_complement_bin})")
            else:
                self.twos_complement_label.setText(f"2's: {masked_decimal}")

            # Apply 4-bit grouping to binary value
            for i, bit in enumerate(reversed(bin_value)):
                grouped_bin = bit + grouped_bin
                if (i + 1) % 4 == 0 and i != len(bin_value) - 1:
                    grouped_bin = " " + grouped_bin

            # Apply conditional grouping to hexadecimal value
            if self.current_bit_width == 8:
                group_size = 2
            else:  # 16-bit or 32-bit
                group_size = 4

            for i in range(len(hex_value) - 1, -1, -1):
                grouped_hex = hex_value[i] + grouped_hex
                if (len(hex_value) - 1 - i + 1) % group_size == 0 and i != 0:
                    grouped_hex = " " + grouped_hex

            self.hex_label.setText(f"${grouped_hex}")
            self.dec_label.setText(dec_value)
            self.bin_label.setText(f"%{grouped_bin}")

        except ValueError:
            self.hex_label.setText("$Invalid Input")
            self.dec_label.setText("Invalid Input")
            self.bin_label.setText("%Invalid Input")
            self.twos_complement_label.setText("2's: Invalid")

    def handle_input(self, key):
        if self.clear_input:
            self.input_field.clear()
            self.clear_input = False

        current_text = self.input_field.text()

        if self.current_input_mode == "hex":
            if key in "0123456789ABCDEFabcdef.()+-*/&|^<>":
                self.input_field.setText(current_text + key.upper())
        elif self.current_input_mode == "bin":
            if key in "01.()+-*/&|^<>":
                self.input_field.setText(current_text + key)
        else: # decimal
            if key in "0123456789.()+-*/&|^<>":
                self.input_field.setText(current_text + key)

        if key == "=":
            self.perform_equals()

    def operation_clicked(self, operation):
        current_text = self.input_field.text()
        self.input_field.setText(f"{current_text} {operation} ")

    def perform_xor(self):
        pass # To be implemented

    def perform_shift_left(self):
        current_text = self.input_field.text().strip()
        try:
            if self.current_input_mode == "hex":
                value = int(current_text, 16)
            elif self.current_input_mode == "bin":
                value = int(current_text, 2)
            else: # decimal
                value = int(current_text)

            shifted_value = value << 1
            mask = (1 << self.current_bit_width) - 1
            masked_result = shifted_value & mask

            self.update_labels(str(masked_result) if self.current_input_mode == "dec" else (hex(masked_result)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(masked_result)[2:].zfill(self.current_bit_width)))
            self.error_label.setText("")
            self.clear_input = True

        except ValueError:
            self.error_label.setText("The Shift Left (<<) operation can only be performed on a single number, not an expression.")

    def perform_shift_right(self):
        current_text = self.input_field.text().strip()
        try:
            if self.current_input_mode == "hex":
                value = int(current_text, 16)
            elif self.current_input_mode == "bin":
                value = int(current_text, 2)
            else: # decimal
                value = int(current_text)

            shifted_value = value >> 1
            mask = (1 << self.current_bit_width) - 1
            masked_result = shifted_value & mask

            self.update_labels(str(masked_result) if self.current_input_mode == "dec" else (hex(masked_result)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(masked_result)[2:].zfill(self.current_bit_width)))
            self.error_label.setText("")
            self.clear_input = True

        except ValueError:
            self.error_label.setText("The Shift Right (>>) operation can only be performed on a single number, not an expression.")
    
    def perform_not(self):
        current_text = self.input_field.text().strip()
        try:
            if self.current_input_mode == "hex":
                value = int(current_text, 16)
            elif self.current_input_mode == "bin":
                value = int(current_text, 2)
            else: # decimal
                value = int(current_text)

            mask = (1 << self.current_bit_width) - 1
            inverted_value = ~value
            masked_result = inverted_value & mask

            self.update_labels(str(masked_result) if self.current_input_mode == "dec" else (hex(masked_result)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(masked_result)[2:].zfill(self.current_bit_width)))
            self.error_label.setText("")
            self.clear_input = True

        except ValueError:
            self.error_label.setText("The NOT operation can only be performed on a single number, not an expression.")

    def perform_equals(self):
        expression = self.input_field.text().strip()

        if not expression:
            return

        parts = expression.split()

        if len(parts) == 1:
            try:
                if self.current_input_mode == "hex":
                    value = int(parts[0], 16)
                elif self.current_input_mode == "bin":
                    value = int(parts[0], 2)
                else: # decimal
                    value = int(parts[0])
                self.update_labels(str(value) if self.current_input_mode == "dec" else (hex(value)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(value)[2:].zfill(self.current_bit_width)))
                self.error_label.setText("")
                self.clear_input = True
            except ValueError as e:
                print(f"Single operand ValueError: {e}")
                self.error_label.setText("Invalid input format.")
            return

        operators = ["+", "-", "*", "/", "AND", "OR", "XOR", "<<", ">>"]
        operator_found = None
        operator_index = -1

        for op in operators:
            try:
                index = expression.rindex(f" {op} ")
                operator_found = op
                operator_index = index
                break
            except ValueError:
                pass
            if op in ("<<", ">>"):
                try:
                    index = expression.rindex(op)
                    if (index == 0 or not expression[index-1].isalnum()) and \
                       (index + len(op) == len(expression) or not expression[index + len(op)].isalnum()):
                        operator_found = op
                        operator_index = index
                        break
                except ValueError:
                    pass

        if operator_found:
            try:
                if operator_found in ("<<", ">>"):
                    operand1_str = expression[:operator_index].strip()
                    operand2_str = expression[operator_index + len(operator_found):].strip()
                else:
                    operand1_str = expression[:operator_index].strip()
                    operand2_str = expression[operator_index + len(operator_found) + 1:].strip() # +1 for the space after the operator

                print(f"Operand 1: '{operand1_str}'")
                print(f"Operator: '{operator_found}'")
                print(f"Operand 2: '{operand2_str}'")

                if self.current_input_mode == "hex":
                    operand1 = int(operand1_str, 16)
                    operand2 = int(operand2_str, 16)
                elif self.current_input_mode == "bin":
                    operand1 = int(operand1_str, 2)
                    operand2 = int(operand2_str, 2)
                else: # decimal
                    operand1 = int(operand1_str)
                    operand2 = int(operand2_str)

                result = None
                if operator_found == "+":
                    result = operand1 + operand2
                elif operator_found == "-":
                    result = operand1 - operand2
                elif operator_found == "*":
                    result = operand1 * operand2
                elif operator_found == "/":
                    if operand2 == 0:
                        self.error_label.setText("Division by zero!")
                        return
                    result = operand1 // operand2
                elif operator_found == "AND":
                    result = operand1 & operand2
                elif operator_found == "OR":
                    result = operand1 | operand2
                elif operator_found == "XOR":
                    result = operand1 ^ operand2
                elif operator_found == "<<":
                    result = operand1 << operand2
                elif operator_found == ">>":
                    result = operand1 >> operand2

                if result is not None:
                    mask = (1 << self.current_bit_width) - 1
                    masked_result = result & mask
                    self.update_labels(str(masked_result) if self.current_input_mode == "dec" else (hex(masked_result)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(masked_result)[2:].zfill(self.current_bit_width)))
                    self.error_label.setText("")
                    self.clear_input = True

            except ValueError as e:
                print(f"Operand Conversion ValueError: {e}")
                self.error_label.setText("Invalid operand format in expression.")
            except Exception as e:
                print(f"General Exception: {e}")
                self.error_label.setText(f"An error occurred during evaluation: {e}")

        elif expression:
            try:
                if self.current_input_mode == "hex":
                    value = int(expression, 16)
                elif self.current_input_mode == "bin":
                    value = int(expression, 2)
                else: # decimal
                    value = int(expression)
                self.update_labels(str(value) if self.current_input_mode == "dec" else (hex(value)[2:].upper().zfill(self.current_bit_width // 4) if self.current_input_mode == "hex" else bin(value)[2:].zfill(self.current_bit_width)))
                self.error_label.setText("")
                self.clear_input = True
            except ValueError as e:
                print(f"Final Value ValueError: {e}")
                self.error_label.setText("Invalid input format.")

    def update_display_result(self, value): # Remove this method
        pass

    def update_labels(self, value):
        try:
            if self.current_input_mode == "hex":
                decimal_value = int(value, 16) if value else 0
                binary_value = bin(decimal_value & ((1 << self.current_bit_width) - 1))[2:].upper().zfill(self.current_bit_width) if value else "0".zfill(self.current_bit_width)
            elif self.current_input_mode == "bin":
                decimal_value = int(value, 2) if value else 0
                hex_value = hex(decimal_value & ((1 << self.current_bit_width) - 1))[2:].upper().zfill(self.current_bit_width // 4) if value else "0".zfill(self.current_bit_width // 4)
            else: # decimal
                decimal_value = int(value) if value else 0
                hex_value = hex(decimal_value & ((1 << self.current_bit_width) - 1))[2:].upper().zfill(self.current_bit_width // 4) if value else "0".zfill(self.current_bit_width // 4)
                binary_value = bin(decimal_value & ((1 << self.current_bit_width) - 1))[2:].upper().zfill(self.current_bit_width) if value else "0".zfill(self.current_bit_width)

            self.hex_label.setText(f"${hex_value}")
            self.dec_label.setText(str(decimal_value))
            self.bin_label.setText(f"%{binary_value}")
            self.twos_complement_label.setText(f"2's: {self.to_twos_complement(decimal_value, self.current_bit_width)}")
        except ValueError:
            self.hex_label.setText("$Invalid")
            self.dec_label.setText("Invalid")
            self.bin_label.setText("%Invalid")
            self.twos_complement_label.setText("2's: Invalid")

    def to_twos_complement(self, value, bits):
        if value < 0:
            value = (1 << bits) + value
        return bin(value & ((1 << bits) - 1))[2:].upper().zfill(bits)

    def update_display_result(self, value):
        mask = (1 << self.current_bit_width) - 1
        masked_value = value & mask
        if self.current_input_mode == "hex":
            self.input_field.setText(hex(masked_value)[2:].upper().zfill(self.current_bit_width // 4))
        elif self.current_input_mode == "bin":
            self.input_field.setText(bin(masked_value)[2:].zfill(self.current_bit_width))
        else:
            self.input_field.setText(str(masked_value))
        self.update_labels(self.input_field.text())

    def update_display_result(self, value):
        mask = (1 << self.current_bit_width) - 1
        masked_value = value & mask
        if self.current_input_mode == "hex":
            self.input_field.setText(hex(masked_value)[2:].upper().zfill(self.current_bit_width // 4))
        elif self.current_input_mode == "bin":
            self.input_field.setText(bin(masked_value)[2:].zfill(self.current_bit_width))
        else:
            self.input_field.setText(str(masked_value))
        self.update_labels(self.input_field.text())

    def set_bit_width(self, width):
        self.current_bit_width = width
        for button in self.bit_width_group.buttons():
            if button.text().startswith(f"{width}-bit"):
                button.setChecked(True)
            else:
                button.setChecked(False)
        self.update_labels(self.input_field.text())


    def get_current_value(self):
        current_text = self.input_field.text()
        if self.current_input_mode == "hex":
            return int(current_text, 16) if current_text else 0
        elif self.current_input_mode == "bin":
            return int(current_text, 2) if current_text else 0
        else: # decimal
            return int(current_text) if current_text else 0
        
    def clear_all(self):
        self.input_field.clear()
        self.hex_label.setText("$0")
        self.dec_label.setText("0")
        self.bin_label.setText("%0")
        self.first_operand = None
        self.current_operation = None
        #self.set_default_mode()

if __name__ == '__main__':
    app = QApplication([])
    converter = BaseConverter()
    converter.show()
    app.exec()
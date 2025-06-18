# As of 2025-04-14 at 03:08 PM, this version is exactly the same as new_design6_2.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGridLayout, QPushButton, QButtonGroup, QRadioButton
)
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

class BaseConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("C-64 Programmer's Calculator")
        # self.setGeometry(100, 100, 400, 300) # Removed fixed geometry for centering

        self.current_input_mode = "dec"
        self.first_operand = None
        self.current_operation = None
        self.current_bit_width = 16  # Default bit width

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)
        # self.input_field.textChanged.connect(self.update_labels) # Disconnected to prevent reset after '='

        self.hex_label = QLabel("$0")
        self.dec_label = QLabel("0")
        self.bin_label = QLabel("%0")

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

        # Bit Width Selection Buttons (REPLACE THESE LINES)
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

        bit_width_layout = QHBoxLayout()
        bit_width_layout.addWidget(self.bit_width_8)
        bit_width_layout.addWidget(self.bit_width_16)
        bit_width_layout.addWidget(self.bit_width_32)

        # Operation Buttons
        self.add_button = QPushButton("+")
        print(f"Add button: {self.add_button}")
        self.subtract_button = QPushButton("-")
        self.multiply_button = QPushButton("*")
        self.divide_button = QPushButton("/")
        self.and_button = QPushButton("AND")
        self.or_button = QPushButton("OR")
        self.xor_button = QPushButton("XOR")
        self.shift_left_button = QPushButton("SHL")
        self.shift_right_button = QPushButton("SHR")
        self.not_button = QPushButton("NOT")
        self.equals_button = QPushButton("=")
        self.clear_button = QPushButton("Clear")
        self.backspace_button = QPushButton("Backspace")

        # Connect Operation Buttons
        self.bit_width_8.clicked.connect(lambda: self.set_bit_width(8))
        self.bit_width_16.clicked.connect(lambda: self.set_bit_width(16))
        self.bit_width_32.clicked.connect(lambda: self.set_bit_width(32))
        self.add_button.clicked.connect(lambda: self.operation_clicked("+"))
        self.subtract_button.clicked.connect(lambda: self.operation_clicked("-"))
        self.multiply_button.clicked.connect(lambda: self.operation_clicked("*"))
        self.divide_button.clicked.connect(lambda: self.operation_clicked("/"))
        self.and_button.clicked.connect(lambda: self.operation_clicked("AND"))
        self.or_button.clicked.connect(lambda: self.operation_clicked("OR"))
        self.xor_button.clicked.connect(lambda: self.operation_clicked("XOR"))
        self.shift_left_button.clicked.connect(lambda: self.operation_clicked("SHL"))
        self.shift_right_button.clicked.connect(lambda: self.operation_clicked("SHR"))
        self.not_button.clicked.connect(self.perform_not)
        self.equals_button.clicked.connect(self.perform_equals)
        self.clear_button.clicked.connect(self.clear_all)
        self.backspace_button.clicked.connect(self.backspace_clicked)

        # Ensure only one bit width button is checked at a time
        self.bit_width_group.buttonClicked.connect(self.update_bit_width_checked)
        
        # Buttons Layout
        buttons_layout = QGridLayout()
        buttons = [
            "A", "B", "C",
            "D", "E", "F",
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            ".", "0", "="
        ]
        row, col = 0, 0
        for label in buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda checked, l=label: self.handle_input(l))
            buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 2:  # Move to the next row after three buttons
                col = 0
                row += 1

        # Operation Buttons Layout (Horizontal)
        op_layout = QHBoxLayout()
        op_layout.addWidget(self.add_button)
        op_layout.addWidget(self.subtract_button)
        op_layout.addWidget(self.multiply_button)
        op_layout.addWidget(self.divide_button)
        op_layout.addWidget(self.and_button)
        op_layout.addWidget(self.or_button)
        op_layout.addWidget(self.xor_button)
        op_layout.addWidget(self.shift_left_button)
        op_layout.addWidget(self.shift_right_button)
        op_layout.addWidget(self.not_button)
        op_layout.addWidget(self.equals_button)
        op_layout.addWidget(self.clear_button)
        op_layout.addWidget(self.backspace_button)

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

        # Main Layout (Vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.hex_label)
        main_layout.addWidget(self.dec_label)
        main_layout.addWidget(self.bin_label)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(bit_width_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(op_layout)

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
            return

        masked_decimal = 0  # Default value

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

            # Apply 4-bit grouping to binary value
            grouped_bin = ""
            for i, bit in enumerate(reversed(bin_value)):
                grouped_bin = bit + grouped_bin
                if (i + 1) % 4 == 0 and i != len(bin_value) - 1:
                    grouped_bin = " " + grouped_bin

            # Apply conditional grouping to hexadecimal value
            grouped_hex = ""
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

    def handle_input(self, key):
        current_text = self.input_field.text()
        if self.current_input_mode == "hex":
            if key in "0123456789ABCDEF":
                self.input_field.setText(current_text + key)
        elif self.current_input_mode == "bin":
            if key in "01":
                self.input_field.setText(current_text + key)
        else: # decimal
            if key in "0123456789.":
                if key == "." and "." in current_text:
                    return  # Only allow one decimal point
                self.input_field.setText(current_text + key)
        self.update_labels(self.input_field.text())

    def operation_clicked(self, operation):
        print(f"Operation button '{operation}' clicked.")
        try:
            current_text = self.input_field.text()
            
            if self.current_input_mode == "hex":
                self.first_operand = int(current_text, 16) if current_text else 0
            elif self.current_input_mode == "bin":
                self.first_operand = int(current_text, 2) if current_text else 0
            else: # decimal
                self.first_operand = int(current_text) if current_text else 0
                
            self.current_operation = operation
            self.update_labels(self.first_operand)
            self.input_field.clear()
        except ValueError:
            self.input_field.setText("Error")
            self.first_operand = None
            self.current_operation = None

    def perform_xor(self):
        pass # To be implemented

    def perform_shift_left(self):
        pass # To be implemented

    def perform_shift_right(self):
        pass # To be implemented
    
    def perform_not(self):
        print(f"Current bit width: {self.current_bit_width}")
        current_text = self.input_field.text()
        try:
            if self.current_input_mode == "hex":
                value = int(current_text, 16) if current_text else 0
            elif self.current_input_mode == "bin":
                value = int(current_text, 2) if current_text else 0
            else:  # decimal
                value = int(current_text) if current_text else 0

            mask = (1 << self.current_bit_width) - 1
            inverted_value = ~value
            masked_result = inverted_value & mask

            hex_format_width = self.current_bit_width // 4
            bin_format_width = self.current_bit_width

            if self.current_input_mode == "hex":
                self.input_field.setText(hex(masked_result)[2:].upper().zfill(hex_format_width))
            elif self.current_input_mode == "bin":
                self.input_field.setText(bin(masked_result)[2:].zfill(bin_format_width))
            else:  # decimal
                self.input_field.setText(str(masked_result))

            self.update_labels(self.input_field.text())

        except ValueError:
            self.input_field.setText("Error")
            self.update_labels("Error")

    def perform_equals(self):
        print("Equals button clicked!")
        if self.first_operand is not None and self.current_operation:
            try:
                second_operand_text = self.input_field.text()
                if self.current_input_mode == "hex":
                    second_operand = int(second_operand_text, 16) if second_operand_text else 0
                elif self.current_input_mode == "bin":
                    second_operand = int(second_operand_text, 2) if second_operand_text else 0
                else: # decimal
                    second_operand = int(second_operand_text) if second_operand_text else 0

                result = None
                if self.current_operation == "+":
                    result = self.first_operand + second_operand
                elif self.current_operation == "-":
                    result = self.first_operand - second_operand
                elif self.current_operation == "*":
                    result = self.first_operand * second_operand
                elif self.current_operation == "/":
                    if second_operand == 0:
                        self.input_field.setText("Error")
                        self.update_labels("Error")
                        return
                    result = self.first_operand // second_operand # Integer division
                elif self.current_operation == "AND":
                    result = self.first_operand & second_operand
                elif self.current_operation == "OR":
                    result = self.first_operand | second_operand
                elif self.current_operation == "XOR":
                    result = self.first_operand ^ second_operand
                elif self.current_operation == "SHL":
                    result = self.first_operand << second_operand
                elif self.current_operation == "SHR":
                    result = self.first_operand >> second_operand

                if result is not None:
                    mask = (1 << self.current_bit_width) - 1
                    masked_result = result & mask
                    if self.current_input_mode == "hex":
                        self.input_field.setText(hex(masked_result)[2:].upper().zfill(self.current_bit_width // 4))
                    elif self.current_input_mode == "bin":
                        self.input_field.setText(bin(masked_result)[2:].zfill(self.current_bit_width))
                    else:
                        self.input_field.setText(str(masked_result))
                    self.update_labels(self.input_field.text())

                self.first_operand = None
                self.current_operation = None

            except ValueError:
                self.input_field.setText("Error")
                self.update_labels("Error")
                self.first_operand = None
                self.current_operation = None
        else:
            # No operation was set, just update labels with current input
            self.update_labels(self.input_field.text())

        print("result: ", result)

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
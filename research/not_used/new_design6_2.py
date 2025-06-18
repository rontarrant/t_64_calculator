from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGridLayout, QPushButton
)
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

class BaseConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C-64 Programmer's Calculator")

        # Single Input Field
        self.input_field = QLineEdit()
        #self.input_field.textChanged.connect(self.update_labels)

        # Display Labels for Different Bases
        self.hex_label = QLabel("$0")
        self.dec_label = QLabel("0")
        self.bin_label = QLabel("%0")

        # Mode Buttons
        self.hex_mode_button = QPushButton("Hex")
        self.dec_mode_button = QPushButton("Dec")
        self.bin_mode_button = QPushButton("Bin")
        self.hex_mode_button.setCheckable(True)
        self.dec_mode_button.setCheckable(True)
        self.bin_mode_button.setCheckable(True)
        self.mode_group = [self.hex_mode_button, self.dec_mode_button, self.bin_mode_button]
        for button in self.mode_group:
            button.setAutoExclusive(True)
            button.clicked.connect(self.set_input_mode)
        self.current_input_mode = "dec" # Default mode

        # Operation Buttons
        self.add_button = QPushButton("+")
        self.subtract_button = QPushButton("-")
        self.multiply_button = QPushButton("*")
        self.divide_button = QPushButton("/")
        self.and_button = QPushButton("AND")
        self.or_button = QPushButton("OR")
        self.not_button = QPushButton("NOT")
        self.equals_button = QPushButton("=")
        self.clear_button = QPushButton("Clear")

        self.add_button.clicked.connect(lambda: self.operation_clicked("+"))
        self.subtract_button.clicked.connect(lambda: self.operation_clicked("-"))
        self.multiply_button.clicked.connect(lambda: self.operation_clicked("*"))
        self.divide_button.clicked.connect(lambda: self.operation_clicked("/"))
        self.and_button.clicked.connect(lambda: self.operation_clicked("AND"))
        self.or_button.clicked.connect(lambda: self.operation_clicked("OR"))
        self.not_button.clicked.connect(self.perform_not)
        self.equals_button.clicked.connect(self.perform_equals)
        self.clear_button.clicked.connect(self.clear_all)

        # Store the first operand and the operation
        self.first_operand = None
        self.current_operation = None

        # Number/Hex Buttons Layout
        buttons_layout = QGridLayout()
        button_labels = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', None, None,
            'A', 'B', 'C',
            'D', 'E', 'F'
        ]
        row, col = 0, 0
        for label in button_labels:
            if label is not None:
                button = QPushButton(label)
                button.clicked.connect(lambda checked, l=label: self.input_field.insert(l))
                buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 2 and row < 3:
                col = 0
                row += 1
            elif col > 2 and row >= 3:
                col = 0
                row += 1

        # Operation Buttons Layout
        op_layout = QHBoxLayout()
        op_layout.addWidget(self.add_button)
        op_layout.addWidget(self.subtract_button)
        op_layout.addWidget(self.multiply_button)
        op_layout.addWidget(self.divide_button)
        op_layout.addWidget(self.and_button)
        op_layout.addWidget(self.or_button)
        op_layout.addWidget(self.not_button)
        op_layout.addWidget(self.equals_button)
        op_layout.addWidget(self.clear_button)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        bases_layout = QHBoxLayout()
        bases_layout.addWidget(QLabel("Hex:"))
        bases_layout.addWidget(self.hex_label)
        bases_layout.addWidget(QLabel("Dec:"))
        bases_layout.addWidget(self.dec_label)
        bases_layout.addWidget(QLabel("Bin:"))
        bases_layout.addWidget(self.bin_label)
        main_layout.addLayout(bases_layout)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.hex_mode_button)
        mode_layout.addWidget(self.dec_mode_button)
        mode_layout.addWidget(self.bin_mode_button)
        main_layout.addLayout(mode_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(op_layout)

        self.setLayout(main_layout)
        self.set_default_mode()

    def set_default_mode(self):
        self.dec_mode_button.setChecked(True)
        self.set_input_mode()

    def set_input_mode(self):
        checked_button = None
        for button in self.mode_group:
            if button.isChecked():
                checked_button = button
                break
        if checked_button:
            self.current_input_mode = checked_button.text().lower()
            validator = None
            if self.current_input_mode == "hex":
                regex = QRegularExpression("[0-9a-fA-F]*")
                validator = QRegularExpressionValidator(regex)
            elif self.current_input_mode == "bin":
                regex = QRegularExpression("[01]*")
                validator = QRegularExpressionValidator(regex)
            else: # decimal
                validator = QIntValidator()
            self.input_field.setValidator(validator)

    def update_labels(self, value):
        print(f"update_labels called with value: '{value}' (type: {type(value)})")
        decimal_value = 0
        if isinstance(value, str):
            text = value
            if not text:
                self.hex_label.setText("$0")
                self.dec_label.setText("0")
                self.bin_label.setText("%0")
                return
            try:
                if self.current_input_mode == "hex":
                    decimal_value = int(text, 16)
                elif self.current_input_mode == "bin":
                    decimal_value = int(text, 2)
                else: # decimal
                    decimal_value = int(text)
            except ValueError:
                self.hex_label.setText("$Error")
                self.dec_label.setText("Error")
                self.bin_label.setText("%Error")
                return
        elif isinstance(value, int):
            decimal_value = value
        else:
            self.hex_label.setText("$Error")
            self.dec_label.setText("Error")
            self.bin_label.setText("%Error")
            return

        hex_value = hex(decimal_value)[2:].upper()
        bin_value = bin(decimal_value)[2:]

        self.hex_label.setText(f"${hex_value}")
        self.dec_label.setText(str(decimal_value))
        self.bin_label.setText(f"%{bin_value}")

    def operation_clicked(self, operation):
        try:
            current_text = self.input_field.text()
            if self.current_input_mode == "hex":
                self.first_operand = int(current_text, 16) if current_text else 0
            elif self.current_input_mode == "bin":
                self.first_operand = int(current_text, 2) if current_text else 0
            else: # decimal
                self.first_operand = int(current_text) if current_text else 0
            self.current_operation = operation
            self.update_labels(self.first_operand) # Update labels with the first operand
            self.input_field.clear()
        except ValueError:
            self.input_field.setText("Error")
            self.first_operand = None
            self.current_operation = None

    def perform_not(self):
        try:
            if self.current_input_mode == "hex":
                operand = int(self.input_field.text(), 16)
            elif self.current_input_mode == "bin":
                operand = int(self.input_field.text(), 2)
            else: # decimal
                operand = int(self.input_field.text())

            # Perform NOT (assuming bit length of input)
            bin_operand = bin(operand)[2:]
            num_bits = len(bin_operand) if bin_operand else 8 # Default to 8 if empty
            mask = (1 << num_bits) - 1
            result = ~operand & mask
            self.update_labels(str(result)) # Update labels with the decimal result
            self.input_field.clear()
            self.first_operand = None
            self.current_operation = None

        except ValueError:
            self.input_field.setText("Error")
            self.first_operand = None
            self.current_operation = None

    def perform_equals(self):
        if self.first_operand is None or self.current_operation is None:
            return

        try:
            second_operand = 0
            current_text = self.input_field.text()
            if self.current_input_mode == "hex":
                second_operand = int(current_text, 16) if current_text else 0
            elif self.current_input_mode == "bin":
                second_operand = int(current_text, 2) if current_text else 0
            else: # decimal
                second_operand = int(current_text) if current_text else 0

            result = 0
            if self.current_operation == "+":
                result = self.first_operand + second_operand
            elif self.current_operation == "-":
                result = self.first_operand - second_operand
            elif self.current_operation == "*":
                result = self.first_operand * second_operand
            elif self.current_operation == "/":
                if second_operand == 0:
                    self.input_field.setText("Div by 0")
                    return
                result = self.first_operand // second_operand # Integer division
            elif self.current_operation == "AND":
                result = self.first_operand & second_operand
            elif self.current_operation == "OR":
                result = self.first_operand | second_operand

            self.update_labels(result) # Pass the integer result directly
            self.first_operand = None
            self.current_operation = None
            self.input_field.clear()

        except ValueError:
            self.hex_label.setText("$Error")
            self.dec_label.setText("Error")
            self.bin_label.setText("%Error")
            self.first_operand = None
            self.current_operation = None

        print("result: ", result)
            
    def clear_all(self):
        self.input_field.clear()
        self.hex_label.setText("$0")
        self.dec_label.setText("0")
        self.bin_label.setText("%0")
        self.first_operand = None
        self.current_operation = None
        self.set_default_mode()

if __name__ == '__main__':
    app = QApplication([])
    converter = BaseConverter()
    converter.show()
    app.exec()
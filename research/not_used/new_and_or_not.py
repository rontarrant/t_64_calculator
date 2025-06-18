from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QGridLayout, QPushButton
)
from PySide6.QtCore import Qt

class BaseConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C-64 Programmer's Calculator")

        # Number Base Input/Display
        self.hex_input = QLineEdit()
        self.dec_input = QLineEdit()
        self.bin_input = QLineEdit()

        self.hex_input.setReadOnly(True)
        self.dec_input.setReadOnly(True)
        self.bin_input.setReadOnly(True)

        # Binary Operation Inputs
        self.operand1_input = QLineEdit()
        self.operand2_input = QLineEdit()
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)

        # Binary Grouping
        self.binary_grouping = QComboBox()
        self.binary_grouping.addItem("No Grouping")
        self.binary_grouping.addItem("4-bit")
        self.binary_grouping.addItem("8-bit")
        self.binary_grouping.currentIndexChanged.connect(self.update_binary_display)
        self.current_binary_grouping = "No Grouping"

        # Mode and Action Buttons
        self.hex_mode_button = QPushButton("Hex Mode")
        self.dec_mode_button = QPushButton("Dec Mode")
        self.bin_mode_button = QPushButton("Bin Mode")
        self.clear_button = QPushButton("Clear")
        self.and_button = QPushButton("AND")
        self.or_button = QPushButton("OR")
        self.not_button = QPushButton("NOT")

        self.hex_mode_button.setCheckable(True)
        self.dec_mode_button.setCheckable(True)
        self.bin_mode_button.setCheckable(True)
        self.hex_mode_button.setAutoExclusive(True)
        self.dec_mode_button.setAutoExclusive(True)
        self.bin_mode_button.setAutoExclusive(True)

        self.hex_mode_button.clicked.connect(lambda: self.set_input_mode("hex"))
        self.dec_mode_button.clicked.connect(lambda: self.set_input_mode("dec"))
        self.bin_mode_button.clicked.connect(lambda: self.set_input_mode("bin"))
        self.clear_button.clicked.connect(self.clear_all)
        self.and_button.clicked.connect(self.perform_and)
        self.or_button.clicked.connect(self.perform_or)
        self.not_button.clicked.connect(self.perform_not)

        self.current_input_mode = None

        # Layouts
        main_layout = QVBoxLayout()

        # Base Conversion Layout
        base_layout = QVBoxLayout()
        base_layout.addWidget(QLabel("Base Conversion:"))
        base_layout.addLayout(self.create_labeled_input("Hexadecimal ($):", self.hex_input))
        base_layout.addLayout(self.create_labeled_input("Decimal:", self.dec_input))
        base_layout.addLayout(self.create_labeled_input("Binary (%):", self.bin_input))
        #base_layout.addWidget(self.create_labeled_widget("Binary Grouping:", self.binary_grouping))
        base_layout.addLayout(self.create_labeled_widget("Binary Grouping:", self.binary_grouping))
        main_layout.addLayout(base_layout)

        # Mode and Clear Buttons Layout
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.hex_mode_button)
        mode_layout.addWidget(self.dec_mode_button)
        mode_layout.addWidget(self.bin_mode_button)
        mode_layout.addWidget(self.clear_button)
        main_layout.addLayout(mode_layout)

        # Binary Operations Layout
        binary_op_layout = QVBoxLayout()
        binary_op_layout.addWidget(QLabel("Binary Operations:"))
        binary_op_layout.addLayout(self.create_labeled_input("Operand 1 (Binary): %", self.operand1_input))
        binary_op_layout.addLayout(self.create_labeled_input("Operand 2 (Binary): %", self.operand2_input))
        binary_op_layout.addLayout(self.create_labeled_input("Result (Binary): %", self.result_input))
        op_buttons_layout = QHBoxLayout()
        op_buttons_layout.addWidget(self.and_button)
        op_buttons_layout.addWidget(self.or_button)
        op_buttons_layout.addWidget(self.not_button)
        binary_op_layout.addLayout(op_buttons_layout)
        main_layout.addLayout(binary_op_layout)

        # Number Buttons Layout (moved to the bottom)
        buttons_layout = QGridLayout()
        button_labels = [
            '7', '8', '9', 'A', 'B',
            '4', '5', '6', 'C', 'D',
            '1', '2', '3', 'E', 'F',
            '0', None, None, None, None
        ]
        row, col = 0, 0
        for label in button_labels:
            if label is not None:
                button = QPushButton(label)
                button.clicked.connect(lambda checked, l=label: self.button_clicked(l))
                buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def create_labeled_input(self, label_text, input_widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(input_widget)
        return layout

    def create_labeled_widget(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def clear_all(self):
        self.hex_input.clear()
        self.dec_input.clear()
        self.bin_input.clear()
        self.operand1_input.clear()
        self.operand2_input.clear()
        self.result_input.clear()
        self.hex_mode_button.setChecked(False)
        self.dec_mode_button.setChecked(False)
        self.bin_mode_button.setChecked(False)
        self.current_input_mode = None
        self.dec_input.setFocus()

    def set_input_mode(self, mode):
        self.current_input_mode = mode
        if mode == "hex":
            self.hex_input.setReadOnly(False)
            self.dec_input.setReadOnly(True)
            self.bin_input.setReadOnly(True)
            self.hex_input.setFocus()
        elif mode == "dec":
            self.hex_input.setReadOnly(True)
            self.dec_input.setReadOnly(False)
            self.bin_input.setReadOnly(True)
            self.dec_input.setFocus()
        elif mode == "bin":
            self.hex_input.setReadOnly(True)
            self.dec_input.setReadOnly(True)
            self.bin_input.setReadOnly(False)
            self.bin_input.setFocus()

    def perform_and(self):
        bin1_text = self.operand1_input.text().lstrip('%').replace(' ', '')
        bin2_text = self.operand2_input.text().lstrip('%').replace(' ', '')
        if not bin1_text or not bin2_text:
            self.result_input.setText("%")
            return
        try:
            int1 = int(bin1_text, 2)
            int2 = int(bin2_text, 2)
            result_int = int1 & int2
            result_bin = bin(result_int)[2:]
            # Ensure consistent bit length (e.g., pad with leading zeros if needed)
            max_len = max(len(bin1_text), len(bin2_text), len(result_bin))
            result_bin = result_bin.zfill(max_len)
            self.result_input.setText(f"%{self.format_binary(result_bin)}")
            self._update_base_conversion(result_int)
        except ValueError:
            self.result_input.setText("%Error")

    def perform_or(self):
        bin1_text = self.operand1_input.text().lstrip('%').replace(' ', '')
        bin2_text = self.operand2_input.text().lstrip('%').replace(' ', '')
        if not bin1_text or not bin2_text:
            self.result_input.setText("%")
            return
        try:
            int1 = int(bin1_text, 2)
            int2 = int(bin2_text, 2)
            result_int = int1 | int2
            result_bin = bin(result_int)[2:]
            max_len = max(len(bin1_text), len(bin2_text), len(result_bin))
            result_bin = result_bin.zfill(max_len)
            self.result_input.setText(f"%{self.format_binary(result_bin)}")
            self._update_base_conversion(result_int)
        except ValueError:
            self.result_input.setText("%Error")

    def perform_not(self):
        bin_text = self.operand1_input.text().lstrip('%').replace(' ', '')
        if not bin_text:
            self.result_input.setText("%")
            return
        try:
            int_val = int(bin_text, 2)
            # Perform NOT based on the bit length of the input
            num_bits = len(bin_text)
            mask = (1 << num_bits) - 1
            result_int = ~int_val & mask
            result_bin = bin(result_int)[2:].zfill(num_bits)
            self.result_input.setText(f"%{self.format_binary(result_bin)}")
            self._update_base_conversion(result_int)
        except ValueError:
            self.result_input.setText("%Error")

    def _update_base_conversion(self, decimal_value):
        hexadecimal_value = hex(decimal_value)[2:].upper()
        binary_value = bin(decimal_value)[2:]
        self.hex_input.setText(f"${hexadecimal_value}")
        self.dec_input.setText(str(decimal_value))
        self.bin_input.setText(f"%{self.format_binary(binary_value)}")

    def format_binary(self, binary_string):
        grouping = self.current_binary_grouping
        if grouping == "No Grouping":
            return binary_string
        elif grouping == "4-bit":
            return " ".join(binary_string[i:i+4] for i in range(0, len(binary_string), 4))
        elif grouping == "8-bit":
            return " ".join(binary_string[i:i+8] for i in range(0, len(binary_string), 8))
        return binary_string

    def update_binary_display(self, index):
        self.current_binary_grouping = self.binary_grouping.itemText(index)
        current_bin_text = self.bin_input.text()
        if current_bin_text.startswith('%'):
            current_bin_text = current_bin_text[1:]
        try:
            if current_bin_text:
                decimal_value = int(current_bin_text.replace(" ", ""), 2)
                formatted_binary = self.format_binary(bin(decimal_value)[2:])
                self.bin_input.setText(f"%{formatted_binary}")
        except ValueError:
            pass

    def update_displays(self, hex_val="", dec_val="", bin_val_raw=""):
        self.hex_input.setText(hex_val)
        self.dec_input.setText(dec_val)
        self.bin_input.setText(f"%{self.format_binary(bin_val_raw)}")

    def button_clicked(self, label):
        focused_widget = self.focusWidget()
        print(f"Button '{label}' clicked.")
        print(f"Focused widget: {focused_widget}")

        if focused_widget == self.hex_input:
            current_hex = self.hex_input.text().lstrip('$')
            new_hex = current_hex + label
            try:
                int(new_hex, 16)
                self.hex_input.setText('$' + new_hex.upper())
                self.hex_changed('$' + new_hex)
            except ValueError:
                pass
        elif focused_widget == self.dec_input:
            if label.isdigit():
                current_dec = self.dec_input.text()
                new_dec = current_dec + label
                try:
                    int(new_dec)
                    self.dec_input.setText(new_dec)
                    self.dec_changed(new_dec)
                except ValueError:
                    pass
        elif focused_widget == self.bin_input:
            if label in ['0', '1']:
                current_bin = self.bin_input.text().lstrip('%').replace(' ', '')
                new_bin = current_bin + label
                self.bin_input.setText('%' + new_bin)
                self.bin_changed('%' + new_bin)
        elif focused_widget == self.operand1_input:
            if label in ['0', '1']:
                current_operand = self.operand1_input.text().lstrip('%').replace(' ', '')
                new_operand = current_operand + label
                self.operand1_input.setText('%' + new_operand)
                print(f"Operand 1 updated: {self.operand1_input.text()}") # Debug print
        elif focused_widget == self.operand2_input:
            if label in ['0', '1']:
                current_operand = self.operand2_input.text().lstrip('%').replace(' ', '')
                new_operand = current_operand + label
                self.operand2_input.setText('%' + new_operand)
                print(f"Operand 2 updated: {self.operand2_input.text()}") # Debug print
        else:
            print("No relevant input field focused for this button.") # Debug print

    def hex_changed(self, text):
        if not text:
            self.update_displays()
            return
        if text.startswith('$'):
            text = text[1:]
        try:
            decimal_value = int(text, 16)
            binary_value = bin(decimal_value)[2:]
            self.update_displays(f"${text.upper()}", str(decimal_value), binary_value)
        except ValueError:
            pass

    def dec_changed(self, text):
        if not text:
            self.update_displays()
            return
        try:
            decimal_value = int(text)
            hexadecimal_value = hex(decimal_value)[2:].upper()
            binary_value = bin(decimal_value)[2:]
            self.update_displays(f"${hexadecimal_value}", text, binary_value)
        except ValueError:
            pass

    def bin_changed(self, text):
        if not text:
            self.update_displays()
            return
        if text.startswith('%'):
            text = text[1:]
        try:
            decimal_value = int(text.replace(" ", ""), 2)
            hexadecimal_value = hex(decimal_value)[2:].upper()
            binary_value = bin(decimal_value)[2:]
            self.update_displays(f"${hexadecimal_value}", str(decimal_value), text.replace(" ", ""))
        except ValueError:
            pass

if __name__ == '__main__':
    app = QApplication([])
    converter = BaseConverter()
    converter.show()
    app.exec()
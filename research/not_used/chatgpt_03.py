import sys
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programmer's Calculator")
        self.setGeometry(100, 100, 400, 400)

        # Setup settings for saving window position
        self.settings = QSettings("MyCompany", "ProgrammerCalculator")
        
        # Initialize UI components
        self.digit_buttons = []  # List to store references to digit buttons
        self.input_field = QLineEdit(self)  # The input field for the user to enter numbers
        self.hex_output = QLineEdit(self)  # HEX output field (read-only)
        self.dec_output = QLineEdit(self)  # DEC output field (read-only)
        self.bin_output = QLineEdit(self)  # BIN output field (read-only)
        
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QGridLayout()

        # Input field at the top
        self.input_field.setReadOnly(False)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.input_field, 0, 0, 1, 4)

        # Output fields (read-only)
        self.hex_output.setReadOnly(True)
        self.dec_output.setReadOnly(True)
        self.bin_output.setReadOnly(True)
        self.hex_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dec_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.bin_output.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.hex_output, 1, 0, 1, 4)
        layout.addWidget(self.dec_output, 2, 0, 1, 4)
        layout.addWidget(self.bin_output, 3, 0, 1, 4)

        # Add mode buttons (HEX, DEC, BIN)
        self.hex_button = QPushButton("HEX", self)
        self.hex_button.setStyleSheet("background-color: lightgray")  # Default color
        self.hex_button.clicked.connect(lambda: self.on_button_click("HEX"))
        self.dec_button = QPushButton("DEC", self)
        self.dec_button.setStyleSheet("background-color: lightgray")  # Default color
        self.dec_button.clicked.connect(lambda: self.on_button_click("DEC"))
        self.bin_button = QPushButton("BIN", self)
        self.bin_button.setStyleSheet("background-color: lightgray")  # Default color
        self.bin_button.clicked.connect(lambda: self.on_button_click("BIN"))

        layout.addWidget(self.hex_button, 4, 0)
        layout.addWidget(self.dec_button, 4, 1)
        layout.addWidget(self.bin_button, 4, 2)

        # Create and add digit and dot buttons
        self.add_buttons(layout)

        # Set layout for the window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Restore previous window position and size
        self.restore_window_position()

    def add_buttons(self, layout):
        """Adds buttons for digits, math, and logic to the grid layout."""
        buttons = [
            ('A', 5, 0), ('B', 5, 1), ('C', 5, 2),
            ('D', 6, 0), ('E', 6, 1), ('F', 6, 2),
            ('7', 7, 0), ('8', 7, 1), ('9', 7, 2),
            ('4', 8, 0), ('5', 8, 1), ('6', 8, 2),
            ('1', 9, 0), ('2', 9, 1), ('3', 9, 2),
            ('0', 10, 0),  ('.', 10, 1)
        ]

        self.hex_on_buttons = ['A', 'B', 'C', 'D', 'E', 'F']
        self.hex_off_buttons = ['.']
        self.dec_on_buttons = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        self.dec_off_buttons = ['A', 'B', 'C', 'D', 'E', 'F']
        self.bin_off_buttons = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', '.']
        # Create buttons for digits and operators
        for label, row, col in buttons:
            print("label: ", label, ", row: ", row, ", col: ", col)
            button = QPushButton(label, self)
            button.setFixedSize(70, 50)
            button.clicked.connect(lambda _, label = label: self.on_button_click(label))
            layout.addWidget(button, row, col)

            # Store references to digit buttons for state changes
            if label not in ['.', 'HEX', 'DEC', 'BIN']:
                self.digit_buttons.append(button)
                print("button position in array: ", self.digit_buttons.index(button))

    def set_buttons_state(self, mode):
        """Sets the active/inactive state of the buttons based on the selected mode."""
        if mode == "HEX":
            # Enable buttons 0-9 and A-F, disable dot button
            self.set_button_state_for_range(0, 9, True)  # 0-9
            self.set_button_state_for_range(10, 15, True)  # A-F
            self.set_button_state_for_button('.', False)  # Disable dot button
            self.hex_button.setStyleSheet("background-color: lightgreen")
            self.dec_button.setStyleSheet("background-color: lightgray")
            self.bin_button.setStyleSheet("background-color: lightgray")
        elif mode == "DEC":
            # Enable 0-9 and dot button, disable A-F
            self.set_button_state_for_range(0, 9, True)  # 0-9
            self.set_button_state_for_range(10, 15, False)  # A-F
            self.set_button_state_for_button('.', True)  # Enable dot button
            self.hex_button.setStyleSheet("background-color: lightgray")
            self.dec_button.setStyleSheet("background-color: lightgreen")
            self.bin_button.setStyleSheet("background-color: lightgray")
        elif mode == "BIN":
            # Enable 0 and 1, disable 2-9, A-F, and dot button
            self.set_button_state_for_button('0', True)
            self.set_button_state_for_button('1', True)
            self.set_button_state_for_range(self.bin_off_buttons, False)  # Disable 2-9
            self.set_button_state_for_range('A', 'F', False)  # Disable A-F
            self.set_button_state_for_button('.', False)  # Disable dot button
            self.hex_button.setStyleSheet("background-color: lightgray")
            self.dec_button.setStyleSheet("background-color: lightgray")
            self.bin_button.setStyleSheet("background-color: lightgreen")

    def set_button_state_for_range(self, button_off_array, is_active):
        """Enable or disable a range of buttons based on `is_active`."""
        for button in button_off_array:
            print("button: ", button)
            self.set_button_state_for_button(self.digit_buttons.index(button).text(), is_active)

    def set_button_state_for_button(self, button_label, is_active):
        """Enable or disable a specific button."""
        print("button_label: ", button_label, ", is_active: ", is_active)

        for button in self.digit_buttons:
            if button.text() == button_label:
                button.setEnabled(is_active)

        # Handle the dot button
        if button_label == '.':
            self.input_field.setEnabled(is_active)

    def on_button_click(self, button_label):
        """Handles button clicks."""
        if button_label == "HEX":
            self.set_buttons_state("HEX")
        elif button_label == "DEC":
            self.set_buttons_state("DEC")
        elif button_label == "BIN":
            self.set_buttons_state("BIN")
        else:
            self.handle_digit_input(button_label)

    def handle_digit_input(self, digit):
        """Handles input of a digit or dot."""
        print("handle_digit_input() digit: ", digit)
        current_text = self.input_field.text()
        new_text = current_text + digit
        self.input_field.setText(new_text)

        # Update outputs based on the current input
        self.update_outputs(new_text)

    def update_outputs(self, input_text):
        """Update HEX, DEC, and BIN output fields."""
        try:
            if input_text != "":
                decimal_value = int(input_text, 0)  # Automatically detect base
                self.hex_output.setText(hex(decimal_value)[2:].upper())  # Remove '0x' and convert to uppercase
                self.dec_output.setText(str(decimal_value))
                self.bin_output.setText(bin(decimal_value)[2:])  # Remove '0b'
            else:
                self.hex_output.clear()
                self.dec_output.clear()
                self.bin_output.clear()
        except ValueError:
            self.hex_output.setText("Invalid")
            self.dec_output.setText("Invalid")
            self.bin_output.setText("Invalid")

    def restore_window_position(self):
        """Restores the window's position and size from settings."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        """Save the window's position and size when closing."""
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QPushButton
from PySide6.QtCore import QSettings
import re

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Programmer\'s Calculator')
        self.resize(300, 400)

        main_layout = QVBoxLayout()

        # Input field for the user to enter a value
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Enter a number (dec/hex/bin)")

        # Labels to display conversion results (Hex, Dec, Bin)
        self.hex_line = QLineEdit(self)
        self.dec_line = QLineEdit(self)
        self.bin_line = QLineEdit(self)

        # Set the result fields as read-only
        self.hex_line.setReadOnly(True)
        self.dec_line.setReadOnly(True)
        self.bin_line.setReadOnly(True)

        # Connect input field change to update conversions
        self.input_line.textChanged.connect(self.update_conversions)

        # Add widgets to the main layout
        main_layout.addWidget(self.input_line)
        main_layout.addWidget(QLabel('Hex:'))
        main_layout.addWidget(self.hex_line)
        main_layout.addWidget(QLabel('Dec:'))
        main_layout.addWidget(self.dec_line)
        main_layout.addWidget(QLabel('Bin:'))
        main_layout.addWidget(self.bin_line)

        # Add grid layout for buttons
        button_grid = QGridLayout()
        self.add_buttons(button_grid)
        main_layout.addLayout(button_grid)

        self.setLayout(main_layout)

        # Restore window state
        self.restore_window_state()

    def add_buttons(self, layout):
        """Adds buttons for digits, math, and logic to the grid layout."""
        # Define button positions
        buttons = [
            ('HEX', 0, 0), ('DEC', 0, 1), ('BIN', 0, 2),  # Control buttons
            ('D', 1, 0), ('E', 1, 1), ('F', 1, 2),       # Hex digits
            ('A', 2, 0), ('B', 2, 1), ('C', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2),
            ('0', 6, 0), ('.', 6, 1),                    # Zero and decimal point
        ]

        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet("font-size: 18px;")  # Enlarge button text
            button.setFixedSize(70, 50)  # Make buttons square (50x50 pixels)
            button.clicked.connect(lambda _, b=text: self.on_button_click(b))
            layout.addWidget(button, row, col)


    def set_buttons_state(self, mode):
        """Sets the active/inactive state of the buttons based on the selected mode."""
        # Dictionary of button states for HEX, DEC, BIN modes
        button_state = {
            'HEX': {
                'digits': True,  # 0-9 and A-F should be active
                'dot': False,    # Dot button should be inactive
                'invalid_digits': False  # No invalid digits (A-F allowed)
            },
            'DEC': {
                'digits': True,  # 0-9 should be active
                'dot': True,     # Dot button should be active
                'invalid_digits': True  # Disable A-F
            },
            'BIN': {
                'digits': False, # Only 0-1 should be active
                'dot': False,    # Dot button should be inactive
                'invalid_digits': True  # Disable all non-binary digits and A-F
            }
        }

        # Get the current mode's button settings
        settings = button_state.get(mode, {})

        # Set buttons for HEX, DEC, BIN based on the mode
        self.set_button_state_for_range(0, 9, settings['digits'])
        self.set_button_state_for_range(10, 15, settings['invalid_digits'])
        self.set_button_state_for_range(16, 20, settings['invalid_digits'])  # A-F for HEX
        self.set_button_state_for_button('.', settings['dot'])

    def set_button_state_for_range(self, start_index, end_index, is_active):
        """Enable or disable a range of buttons based on `is_active`."""
        for i in range(start_index, end_index + 1):
            button = self.digit_buttons[i]  # Assuming buttons are stored in a list
            button.setEnabled(is_active)

    def set_button_state_for_button(self, button_label, is_active):
        """Enable or disable a specific button."""
        button = self.find_button_by_label(button_label)
        button.setEnabled(is_active)
    def set_button_state_for_range(self, start_index, end_index, is_active):
        """Enable or disable a range of buttons based on `is_active`."""
        for i in range(start_index, end_index + 1):
            button = self.digit_buttons[i]  # Assuming buttons are stored in a list
            button.setEnabled(is_active)

    def set_button_state_for_button(self, button_label, is_active):
        """Enable or disable a specific button."""
        button = self.find_button_by_label(button_label)
        button.setEnabled(is_active)

    def find_button_by_label(self, label):
        """Find and return a button by its label."""
        for button in self.digit_buttons:
            if button.text() == label:
                return button
        return None  # In case the button is not found

    def on_button_click(self, button_label):
        """Handles button clicks."""
        if button_label == "HEX":
            self.set_buttons_state("HEX")
        elif button_label == "DEC":
            self.set_buttons_state("DEC")
        elif button_label == "BIN":
            self.set_buttons_state("BIN")
        else:
            # Handle normal digit or dot button click behavior
            self.handle_digit_input(button_label)

    def handle_digit_input(self, digit):
        """Handles input of a digit or dot."""
        current_text = self.input_field.text()
        new_text = current_text + digit
        self.input_field.setText(new_text)

    def on_button_click(self, button_text):
        """Handles button clicks and updates the input field."""
        if button_text in "0123456789ABCDEF":
            # Append the button's text to the input field
            self.input_line.setText(self.input_line.text() + button_text)

    def restore_window_state(self):
        settings = QSettings("YourCompany", "ProgrammerCalculator")
        geometry = settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)

    def save_window_state(self):
        settings = QSettings("YourCompany", "ProgrammerCalculator")
        settings.setValue("windowGeometry", self.saveGeometry())

    def update_conversions(self):
        # Get input value from QLineEdit
        input_value = self.input_line.text().strip()

        # If input is empty, clear all result fields
        if not input_value:
            self.hex_line.clear()
            self.dec_line.clear()
            self.bin_line.clear()
            return

        # Try to interpret the input value as decimal, hex, or binary
        try:
            if input_value.lower().startswith("0x"):  # Hexadecimal input (with 0x prefix)
                    value = int(input_value, 16)
            elif re.match(r'^[0-9a-fA-F]+$', input_value):  # Hexadecimal input (without 0x prefix)
                    value = int(input_value, 16)
            elif input_value.lower().startswith("0b"):  # Binary input
                    value = int(input_value, 2)
            else:  # Assume decimal input
                    value = int(input_value)

            # Update read-only result fields
            self.hex_line.setText(f"0x{value:X}")  # Uppercase hexadecimal with 0x prefix
            self.dec_line.setText(str(value))
            self.bin_line.setText(f"0b{bin(value)[2:]}")  # Remove '0b' prefix from binary

        except ValueError:
            # If input is invalid, clear the conversion results
            self.hex_line.setText('Invalid')
            self.dec_line.setText('Invalid')
            self.bin_line.setText('Invalid')


    def closeEvent(self, event):
        self.save_window_state()
        super().closeEvent(event)


# Create the app and window
app = QApplication([])
window = ConverterApp()
window.show()
app.exec()

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QSettings
import re

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Programmer\'s Calculator')
        self.resize(300, 200)  # Set default window size

        layout = QVBoxLayout()

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

        # Add widgets to layout
        layout.addWidget(self.input_line)
        layout.addWidget(QLabel('Hex:'))
        layout.addWidget(self.hex_line)
        layout.addWidget(QLabel('Dec:'))
        layout.addWidget(self.dec_line)
        layout.addWidget(QLabel('Bin:'))
        layout.addWidget(self.bin_line)

        self.setLayout(layout)

        # Restore window state
        self.restore_window_state()

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
            self.hex_line.setText(f"0x{value:x}")  # Display hex with 0x prefix
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

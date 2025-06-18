from PySide6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt

class BaseConverter(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("C-64 Programmer's Calculator")

		self.hex_input = QLineEdit()
		self.dec_input = QLineEdit()
		self.bin_input = QLineEdit()

		self.hex_input.textChanged.connect(self.hex_changed)
		self.dec_input.textChanged.connect(self.dec_changed)
		self.bin_input.textChanged.connect(self.bin_changed)

		self.binary_grouping = QComboBox()
		self.binary_grouping.addItem("No Grouping")
		self.binary_grouping.addItem("4-bit")
		self.binary_grouping.addItem("8-bit")
		self.binary_grouping.currentIndexChanged.connect(self.update_binary_display)
		self.current_binary_grouping = "No Grouping"

		hex_layout = QHBoxLayout()
		hex_layout.addWidget(QLabel("Hexadecimal ($):"))
		hex_layout.addWidget(self.hex_input)

		dec_layout = QHBoxLayout()
		dec_layout.addWidget(QLabel("Decimal:"))
		dec_layout.addWidget(self.dec_input)

		bin_layout = QHBoxLayout()
		bin_layout.addWidget(QLabel("Binary (%):"))
		bin_layout.addWidget(self.bin_input)

		grouping_layout = QHBoxLayout()
		grouping_layout.addWidget(QLabel("Binary Grouping:"))
		grouping_layout.addWidget(self.binary_grouping)

		main_layout = QVBoxLayout()
		main_layout.addLayout(hex_layout)
		main_layout.addLayout(dec_layout)
		main_layout.addLayout(bin_layout)
		main_layout.addLayout(grouping_layout)

		self.setLayout(main_layout)

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
				decimal_value = int(current_bin_text.replace(" ", ""), 2) # Remove existing spaces before converting
				formatted_binary = self.format_binary(bin(decimal_value)[2:])
				self.bin_input.setText(f"%{formatted_binary}")
		except ValueError:
			pass # Keep the text as is if it's invalid

	def update_displays(self, hex_val="", dec_val="", bin_val_raw=""):
		self.hex_input.setText(hex_val)
		self.dec_input.setText(dec_val)
		self.bin_input.setText(f"%{self.format_binary(bin_val_raw)}")

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
			# Remove spaces before attempting conversion
			decimal_value = int(text.replace(" ", ""), 2)
			hexadecimal_value = hex(decimal_value)[2:].upper()
			self.update_displays(f"${hexadecimal_value}", str(decimal_value), text.replace(" ", ""))
		except ValueError:
			pass

if __name__ == '__main__':
	app = QApplication([])
	converter = BaseConverter()
	converter.show()
	app.exec()
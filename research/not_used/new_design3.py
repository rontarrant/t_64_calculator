from PySide6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
	QGridLayout, QPushButton
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

		# Number Buttons Layout
		buttons_layout = QGridLayout()
		button_labels = [
			'7', '8', '9', 'A', 'B',
			'4', '5', '6', 'C', 'D',
			'1', '2', '3', 'E', 'F',
			'0', None, None, None, None # None for empty spaces
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

		main_layout = QVBoxLayout()
		main_layout.addLayout(hex_layout)
		main_layout.addLayout(dec_layout)
		main_layout.addLayout(bin_layout)
		main_layout.addLayout(grouping_layout)
		main_layout.addLayout(buttons_layout)

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
				decimal_value = int(current_bin_text.replace(" ", ""), 2)
				formatted_binary = self.format_binary(bin(decimal_value)[2:])
				self.bin_input.setText(f"%{formatted_binary}")
		except ValueError:
			pass

	def update_displays(self, hex_val="", dec_val="", bin_val_raw=""):
		self.hex_input.setText(hex_val)
		self.dec_input.setText(dec_val)
		self.bin_input.setText(f"%{self.format_binary(bin_val_raw)}")

	'''
	def button_clicked(self, label):
		current_hex = self.hex_input.text().lstrip('$')
		current_dec = self.dec_input.text()
		current_bin = self.bin_input.text().lstrip('%').replace(' ', '')

		focused_widget = self.focusWidget()

		if focused_widget == self.hex_input:
			new_hex = current_hex + label
			try:
				int(new_hex, 16) # Check if it's a valid hex character
				self.hex_changed('$' + new_hex)
			except ValueError:
				pass # Ignore invalid hex characters
		elif focused_widget == self.dec_input:
			if label.isdigit():
				new_dec = current_dec + label
				try:
					int(new_dec)
					self.dec_changed(new_dec)
				except ValueError:
					pass # Ignore non-digit characters or values that are too large
		elif focused_widget == self.bin_input:
			if label in ['0', '1']:
				new_bin = current_bin + label
				try:
					int(new_bin, 2)
					self.bin_changed('%' + new_bin)
				except ValueError:
					pass # Should not happen with '0' or '1'
		else:
			# If no specific input field is focused, default to decimal
			if label.isdigit():
				new_dec = current_dec + label
				try:
					int(new_dec)
					self.dec_changed(new_dec)
				except ValueError:
					pass
	'''

	def button_clicked(self, label):
		focused_widget = self.focusWidget()

		if focused_widget == self.hex_input:
			current_hex = self.hex_input.text().lstrip('$')
			new_hex = current_hex + label
			# We don't need to try to convert *immediately* on each button press
			self.hex_input.setText('$' + new_hex.upper())
			self.hex_changed('$' + new_hex)
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
		else:
			# If no specific input field is focused, default to decimal
			if label.isdigit():
				current_dec = self.dec_input.text()
				new_dec = current_dec + label
				try:
					int(new_dec)
					self.dec_input.setText(new_dec)
					self.dec_changed(new_dec)
				except ValueError:
					pass
					 
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
			self.update_displays(f"${hexadecimal_value}", str(decimal_value), text.replace(" ", ""))
		except ValueError:
			pass

if __name__ == '__main__':
	app = QApplication([])
	converter = BaseConverter()
	converter.show()
	app.exec()
	
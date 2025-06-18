from PySide6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
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

		hex_layout = QHBoxLayout()
		hex_layout.addWidget(QLabel("Hexadecimal ($):"))
		hex_layout.addWidget(self.hex_input)

		dec_layout = QHBoxLayout()
		dec_layout.addWidget(QLabel("Decimal:"))
		dec_layout.addWidget(self.dec_input)

		bin_layout = QHBoxLayout()
		bin_layout.addWidget(QLabel("Binary (%):"))
		bin_layout.addWidget(self.bin_input)

		main_layout = QVBoxLayout()
		main_layout.addLayout(hex_layout)
		main_layout.addLayout(dec_layout)
		main_layout.addLayout(bin_layout)

		self.setLayout(main_layout)

	def update_displays(self, hex_val="", dec_val="", bin_val=""):
		self.hex_input.setText(hex_val)
		self.dec_input.setText(dec_val)
		self.bin_input.setText(bin_val)

	def hex_changed(self, text):
		if not text:
			self.update_displays()
			return
		if text.startswith('$'):
			text = text[1:]
		try:
			decimal_value = int(text, 16)
			binary_value = bin(decimal_value)[2:]
			self.update_displays(f"${text.upper()}", str(decimal_value), f"%{binary_value}")
		except ValueError:
			# Optionally handle invalid hexadecimal input (e.g., clear other fields or show an error)
			pass

	def dec_changed(self, text):
		if not text:
			self.update_displays()
			return
		try:
			decimal_value = int(text)
			hexadecimal_value = hex(decimal_value)[2:].upper()
			binary_value = bin(decimal_value)[2:]
			self.update_displays(f"${hexadecimal_value}", text, f"%{binary_value}")
		except ValueError:
			# Optionally handle invalid decimal input
			pass

	def bin_changed(self, text):
		if not text:
			self.update_displays()
			return
		if text.startswith('%'):
			text = text[1:]
		try:
			decimal_value = int(text, 2)
			hexadecimal_value = hex(decimal_value)[2:].upper()
			self.update_displays(f"${hexadecimal_value}", str(decimal_value), f"%{text}")
		except ValueError:
			# Optionally handle invalid binary input
			pass

if __name__ == '__main__':
	app = QApplication([])
	converter = BaseConverter()
	converter.show()
	app.exec()
	
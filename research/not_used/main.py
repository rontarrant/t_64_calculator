import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, 
							 QPushButton, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt

class T64Calculator(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		self.display = QLineEdit()
		self.display.setAlignment(Qt.AlignRight)
		self.display.setReadOnly(True)
		self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		self.hex_button = QPushButton("Hex")
		self.dec_button = QPushButton("Dec")
		self.oct_button = QPushButton("Oct")
		self.bin_button = QPushButton("Bin")
		self.signed_unsigned_button = QPushButton("Signed")
		self.divide_button = QPushButton("/")
		self.multiply_button = QPushButton("*")
		self.subtract_button = QPushButton("-")
		self.add_button = QPushButton("+")
		self.open_bracket_button = QPushButton("(")
		self.close_bracket_button = QPushButton(")")
		self.decimal_point_button = QPushButton(".")
		self.equals_button = QPushButton("=")
		self.clear_button = QPushButton("Clear")
		self.backspace_button = QPushButton("Backspace")
		self.bit8_button = QPushButton("8-bit")
		self.bit16_button = QPushButton("16-bit")
		self.bit32_button = QPushButton("32-bit")

		self.buttons = [
			["Hex", "D", "E", "F", "Signed"],
			["Dec", "A", "B", "C", "/"],
			["Oct", "7", "8", "9", "*"],
			["Bin", "4", "5", "6", "-"],
			["32-bit", "1", "2", "3", "+"],
			["16-bit", "(", "0", ".", ")"],
			["8-bit", "Clear", "=", "Backspace"]
		]

		self.grid = QGridLayout()
		self.grid.addWidget(self.display, 0, 0, 1, 5)

		for row_index, row in enumerate(self.buttons):
			for col_index, button_text in enumerate(row):
				button = getattr(self, f"{button_text.lower().replace('-', '_')}_button", QPushButton(button_text))
				self.grid.addWidget(button, row_index + 1, col_index)
				button.clicked.connect(self.create_button_click_handler(button_text))

		self.setLayout(self.grid)
		self.setWindowTitle("T-64 Calculator")
		self.show()

		self.current_base = 10  # Default to decimal
		self.is_signed = False
		self.bit_size = 32

		self.update_button_states()

	def create_button_click_handler(self, button_text):
		def handle_click():
			if button_text.isdigit() or button_text in "ABCDEF.()+-*/.":
				self.display.setText(self.display.text() + button_text)
			elif button_text == "Clear":
				self.display.clear()
			elif button_text == "Backspace":
				self.display.setText(self.display.text()[:-1])
			elif button_text == "=":
				self.calculate_result()
			elif button_text in ["Hex", "Dec", "Oct", "Bin"]:
				self.set_base(button_text)
			elif button_text in ["8-bit", "16-bit", "32-bit"]:
				self.set_bit_size(int(button_text.split("-")[0]))
			elif button_text == "Signed":
				self.toggle_signed_unsigned()

		return handle_click

	def set_base(self, base_text):
		if base_text == "Hex":
			self.current_base = 16
		elif base_text == "Dec":
			self.current_base = 10
		elif base_text == "Oct":
			self.current_base = 8
		elif base_text == "Bin":
			self.current_base = 2
		self.update_button_states()

	def set_bit_size(self, size):
		self.bit_size = size

	def toggle_signed_unsigned(self):
		self.is_signed = not self.is_signed

		if self.is_signed:
			self.signed_unsigned_button.setText("Unsigned")
		else:
			self.signed_unsigned_button.setText("Signed")

	def update_button_states(self):
		for button_text in "ABCDEF89":
			button = getattr(self, f"{button_text.lower()}_button", None)
			if button:
				button.setEnabled(self.current_base > 10 if button_text in "ABCDEF" else self.current_base > 8 if button_text in "89" else True)

		if self.current_base < 16:
			for button_text in "ABCDEF":
				button = getattr(self, f"{button_text.lower()}_button", None)
				if button:
					button.setEnabled(False)
		if self.current_base < 10:
			for button_text in "89":
				button = getattr(self, f"{button_text.lower()}_button", None)
				if button:
					button.setEnabled(False)
		if self.current_base <2:
			for button_text in "23456789":
				button = getattr(self, f"{button_text.lower()}_button", None)
				if button:
					button.setEnabled(False)

	def calculate_result(self):
		try:
			expression = self.display.text()
			result = eval(expression)
			result = int(result)
			result = self.apply_bit_range(result)
			self.display.setText(expression + " = " + str(result))
		except Exception as e:
			self.display.setText("Error")
			print (e)

	def apply_bit_range(self, result):
		max_unsigned = (1 << self.bit_size) - 1
		max_signed = (1 << (self.bit_size - 1)) - 1
		min_signed = -(1 << (self.bit_size - 1))

		if self.is_signed:
			if result > max_signed:
				result = min_signed + (result - max_signed -1)
			elif result < min_signed:
				result = max_signed - (min_signed - result -1)
		else:
			if result > max_unsigned:
				result %= (max_unsigned + 1)
			elif result < 0:
				result %= (max_unsigned + 1)
		return result

if __name__ == "__main__":
	app = QApplication(sys.argv)
	calculator = T64Calculator()
	sys.exit(app.exec())
	
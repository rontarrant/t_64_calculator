import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from callbacks import *
from c64_palette import C64Palette

active_radio_buttons = {}
numsys = []
bits = []

# specifications for all buttons (except Equals)
base_specs = {
	"width": 140,
	"height": 100,
	"outline": 4,
}

# Fill in the differences between the
# specifications for the 4 button types.
one_line_specs = base_specs.copy()
one_line_specs["font size"] = 36

two_line_specs = base_specs.copy()
two_line_specs["font size"] = 32
two_line_specs["subfont size"] = 14

angled_specs = base_specs.copy()
angled_specs["font size"] = 26
angled_specs["angle"] = -30

equals_specs = base_specs.copy()
equals_specs["width"] = 420
equals_specs["font size"] = 36

button_data = {
	# row 1
 	"bin": {
		"label": "BIN",
		"type": "radio",
		"group": "numsys",
		"palette": C64Palette().numsys,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": set_binary_number_system
		},
 	"dec": {
		 "label": "DEC",
		 "type": "radio",
		 "group": "numsys",
		 "palette": C64Palette().numsys,
		"specs": one_line_specs,
		 "state": "active",
		 "callback": set_decimal_number_system
	},
	"hex": {
		"label": "HEX",
		"type": "radio",
		"group": "numsys",
		"palette": C64Palette().numsys,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": set_hexadecimal_number_system 
	},
	"signed": {
		"label": "+/-",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": toggle_signed
	},
	# row 2
 	"bit_8": {
		"label": "8",
		"sublabel": "BIT",
		"type": "radio",
		"group": "bits",
		"palette": C64Palette().bits,
		"specs": two_line_specs,
		"state": "active",
		"callback": set_8_bit_width
	},
 	"bit_16": {
		"label": "16",
		"sublabel": "BIT",
		"type": "radio",
		"group": "bits",
		"palette": C64Palette().bits,
		"specs": two_line_specs,
		"state": "inactive",
		"callback": set_16_bit_width
		},
 	"bit_32": {
		"label": "32",
		"sublabel": "BIT",
		"type": "radio",
		"group": "bits",
		"palette": C64Palette().bits,
		"specs": two_line_specs,
		"state": "inactive",
		"callback": set_32_bit_width
	},
	"div": {
		"label": "/",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_division
	},
	# row 3
	"d": {
		"label": "D",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_d
	},
	"e": {
		"label": "E",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_e
	},
	"f": {
		"label": "F",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_f
	},
	"multiply": {
		"label": "*",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_multiply
	},
	# row 4
	"a": {
		"label": "A",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_a
	},
	"b": {
		"label": "B",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_b
	},
	"c": {
		"label": "C",
		"type": "hex",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "inactive",
		"callback": insert_c
	},
	"subtract": {
		"label": "-",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_subtract
	},
	# row 5
	"7": {
		"label": "7",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_7
	},
	"8": {
		"label": "8",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_8
	},
	"9": {
		"label": "9",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_9
	},
	"add": {
		"label": "+",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_addition
	},
	# row 6
	"4": {
		"label": "4",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_4
	},
	"5": {
		"label": "5",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_5
	},
	"6": {
		"label": "6",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_6
	},
	"shift_left": {
		"label": "<<",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "active",
		"callback": do_shift_left
	},
	# row 7
	"1": {
		"label": "1",
		"type": "perm",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_1
	},
	"2": {
		"label": "2",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_2
	},
	"3": {
		"label": "3",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_3
	},
	"shift_right": {
		"label": ">>",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "active",
		"callback": do_shift_right
	},
	# row 08
	"clear": {
		"label": "CLR",
		"type": "perm",
		"group": "edit",
		"palette": C64Palette().edit,
		"specs": one_line_specs,
		"state": "always",
		"callback": clear_display
	},
	"0": {
		"label": "0",
		"type": "perm",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "always",
		"callback": insert_0
	},
	"dot": {
		"label": ".",
		"type": "dec",
		"group": "digit",
		"palette": C64Palette().digit,
		"specs": one_line_specs,
		"state": "active",
		"callback": insert_dot
	},
	"backspace": {
		"label": "BS",
		"type": "perm",
		"group": "edit",
		"palette": C64Palette().edit,
		"specs": one_line_specs,
		"state": "always",
		"callback": do_backspace
	},
	# row 09
	"and": {
		"label": "AND",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": do_and
	},
	"or": {
		"label": "OR",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": do_or
	},
	"xor": {
		"label": "XOR",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "active",
		"callback": do_xor
	},
	"not": {
		"label": "NOT",
		"type": "perm",
		"group": "math",
		"palette": C64Palette().math,
		"specs": one_line_specs,
		"state": "always",
		"callback": do_not
	},
	# row 10
	"equals": {
		"label": "=",
		"type": "perm",
		"group": "edit",
		"palette": C64Palette().edit,
		"specs": equals_specs,
		"state": "always",
		"callback": do_equals
	},
	"t64_logo": {
		"label": "T-64",
		"type": "perm",
		"group": "about",
		"palette": C64Palette().about,
		"specs": angled_specs,
		"state": "always",
		"callback": about
	},
} # button_data

if __name__ == "__main__":
	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Button Grid")
			self.layout = QGridLayout(self)
			self.buttons = {}  # To store the created buttons

			button_ids = list(button_data.keys())
			rows = 9
			columns = 4

			for row in range(rows):
				for column in range(columns):
					index = row * columns + column

					if index < len(button_ids):
						button_id = button_ids[index]
						properties = button_data[button_id]
						button_name = properties["label"]

						if properties["group"] == "bits":
							button_sub_name = properties["sublabel"]

						callback_func = properties["callback"]

						button = QPushButton(button_name)
						button.clicked.connect(callback_func)
						self.layout.addWidget(button, row, column)
						self.buttons[button_id] = button
			
			# Easiest way: do the last row separately so
			# the Equals button can span three columns.
			index += 1 # last row, first button
			row += 1
			column = 0
			button_id = button_ids[index]
			properties = button_data[button_id]
			button_name = properties["label"]
			callback_func = properties["callback"]

			button = QPushButton(button_name)
			button.clicked.connect(callback_func)
			self.layout.addWidget(button, row, column, 1, 3)
			self.buttons[button_id] = button

			index += 1 # last row, second button
			column = 3
			button_id = button_ids[index]
			properties = button_data[button_id]
			button_name = properties["label"]
			callback_func = properties["callback"]

			button = QPushButton(button_name)
			button.clicked.connect(callback_func)
			self.layout.addWidget(button, row, column)
			self.buttons[button_id] = button
			self.setLayout(self.layout)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
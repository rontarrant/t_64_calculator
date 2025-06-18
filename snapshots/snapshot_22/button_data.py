import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
										QSizePolicy)
from PySide6.QtGui import QFont
from PySide6.QtCore import QEvent

from c64_palette import C64Palette
from callbacks import *

from button_specs import *

# Data for all buttons (the keys tell the tale)
# Data for all buttons (the keys tell the tale)
button_data = {
# row 1
"bin": {
	"label": "BIN",
	"type": "radio",
	"group": "numsys",
	"palette": C64Palette().numsys,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": handle_numsys_change
	},
"dec": {
	"label": "DEC",
	"type": "radio",
	"group": "numsys",
	"palette": C64Palette().numsys,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "active",
	"callback": handle_numsys_change
},
"hex": {
	"label": "HEX",
	"type": "radio",
	"group": "numsys",
	"palette": C64Palette().numsys,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": handle_numsys_change 
},
"signed": {
	"label": "+/-",
	"type": "perm",
	"group": "signed",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": toggle_signed
},
# row 2
"bit_8": {
	"label": "8-BIT",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "active",
	"callback": handle_bitwidth_change
},
"bit_16": {
	"label": "16-BIT",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": handle_bitwidth_change
	},
"bit_32": {
	"label": "32-BIT",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": handle_bitwidth_change
},
"div": {
	"label": "/",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
# row 3
"d": {
	"label": "D",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"e": {
	"label": "E",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"f": {
	"label": "F",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"multiply": {
	"label": "*",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
# row 4
"a": {
	"label": "A",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"b": {
	"label": "B",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"c": {
	"label": "C",
	"type": "hex",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "inactive",
	"callback": insert_digit
},
"subtract": {
	"label": "-",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
# row 5
"7": {
	"label": "7",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"8": {
	"label": "8",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"9": {
	"label": "9",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"add": {
	"label": "+",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
# row 6
"4": {
	"label": "4",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"5": {
	"label": "5",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"6": {
	"label": "6",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"shift_left": {
	"label": "<<",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "active",
	"callback": set_math_operation
},
# row 7
"1": {
	"label": "1",
	"type": "perm",
	"group": "digit",
	"palette": C64Palette().digit,
	"specs": one_line_specs,
	"state": "always",
	"callback": insert_digit
},
"2": {
	"label": "2",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"3": {
	"label": "3",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"shift_right": {
	"label": ">>",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "active",
	"callback": set_math_operation
},
# row 08
"clear": {
	"label": "CLR",
	"type": "perm",
	"group": "edit",
	"palette": C64Palette().edit,
	"specs": one_line_specs,
	"state": "always",
	"callback": edit_operation
},
"0": {
	"label": "0",
	"type": "perm",
	"group": "digit",
	"palette": C64Palette().digit,
	"specs": one_line_specs,
	"state": "always",
	"callback": insert_digit
},
"dot": {
	"label": ".",
	"type": "dec",
	"group": "digit",
	"palette": C64Palette().digit,
	"inactive_palette": C64Palette().light,
	"specs": one_line_specs,
	"state": "active",
	"callback": insert_digit
},
"backspace": {
	"label": "BS",
	"type": "perm",
	"group": "edit",
	"palette": C64Palette().edit,
	"specs": one_line_specs,
	"state": "always",
	"callback": edit_operation
},
# row 09
"and": {
	"label": "AND",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
"or": {
	"label": "OR",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
},
"xor": {
	"label": "XOR",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "active",
	"callback": set_math_operation
},
"not": {
	"label": "NOT",
	"type": "perm",
	"group": "math",
	"palette": C64Palette().math,
	"specs": one_line_specs,
	"state": "always",
	"callback": set_math_operation
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

	class ResizableButton(QPushButton):
		def __init__(self, text, initial_font_size = 12, parent = None):
			super().__init__(text, parent)
			self.initial_font_size = initial_font_size
			self.font_factor = 0.5  # Adjust this to control how much the font scales
			# We don't need to store _current_font_size or _first_resize anymore

			# Set the initial font (though resizeEvent will likely override this quickly)
			font = self.font()
			font.setPointSize(self.initial_font_size)
			self.setFont(font)

		def resizeEvent(self, event):
			super().resizeEvent(event)
			# Always adjust font size on resize
			self.adjust_font_size()

		def adjust_font_size(self):
			button_width = self.width()
			button_height = self.height()

			available_space = min(button_width, button_height)
			new_font_size = int(available_space * self.font_factor)

			# Ensure a reasonable minimum font size
			if new_font_size < 6:
				new_font_size = 6

			# Always set the font size
			font = self.font()
			font.setPointSize(new_font_size)
			self.setFont(font)
			# No need to update _current_font_size

	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Resizable Button Grid")
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
							callback_func = properties["callback"]
							initial_font_size = properties["specs"].get("font size", 12)

							button = ResizableButton(button_name, initial_font_size=initial_font_size)
							button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
							button.clicked.connect(callback_func)
							self.layout.addWidget(button, row, column)
							self.buttons[button_id] = button

			# Last row - Equals button spans 3 columns
			index = rows * columns
			row = rows
			column = 0
			if index < len(button_ids):
				button_id = button_ids[index]
				properties = button_data[button_id]
				button_name = properties["label"]
				callback_func = properties["callback"]
				initial_font_size = properties["specs"].get("font size", 12)

				button = ResizableButton(button_name, initial_font_size=initial_font_size)
				button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
				button.clicked.connect(callback_func)
				self.layout.addWidget(button, row, column, 1, 3)
				self.buttons[button_id] = button
				index += 1

			# Last row - T-64 logo
			if index < len(button_ids):
				column = 3
				button_id = button_ids[index]
				properties = button_data[button_id]
				button_name = properties["label"]
				callback_func = properties["callback"]
				initial_font_size = properties["specs"].get("font size", 12)

				button = ResizableButton(button_name, initial_font_size=initial_font_size)
				button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
				button.clicked.connect(callback_func)
				self.layout.addWidget(button, row, column)
				self.buttons[button_id] = button

			self.setLayout(self.layout)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
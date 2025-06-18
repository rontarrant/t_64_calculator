import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from callbacks import *
from c64_palette import C64Palette

# specifications used for all buttons except Equals
base_specs = {
"aspect_ratio": 1.4, # Standard aspect ratio (1.4:1)
"outline": 4,
}

# OneLineButton's have their own font size
one_line_specs = base_specs.copy()
one_line_specs["font size"] = 36

# TwoLineButton's have separate font sizes
# for each line of text
two_line_specs = base_specs.copy()
two_line_specs["font size"] = 32
two_line_specs["subfont size"] = 14

# AngledButton (there's only one) has its own font size
# as well as an angle for the text's baseline
angled_specs = base_specs.copy()
angled_specs["font size"] = 26
angled_specs["angle"] = -30
angled_specs["aspect_ratio"] = 1.0 # Example of a different aspect ratio

# Equals: the only button with a unique width (will still respect aspect ratio)
equals_specs = base_specs.copy()
equals_specs["aspect_ratio"] = 4.2 # Three times wider than a standard button
equals_specs["font size"] = 36

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
	"label": "8",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": two_line_specs,
	"state": "active",
	"callback": handle_bitwidth_change
},
"bit_16": {
	"label": "16",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": two_line_specs,
	"state": "inactive",
	"callback": handle_bitwidth_change
	},
"bit_32": {
	"label": "32",
	"sublabel": "BIT",
	"type": "radio",
	"group": "bits",
	"palette": C64Palette().bits,
	"inactive_palette": C64Palette().dark,
	"specs": two_line_specs,
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
	from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
	from PySide6.QtCore import QSize, Qt

	class AspectRatioButton(QPushButton):
		def __init__(self, properties, parent=None, column_span=1):
			super().__init__(properties.get("label", ""), parent)
			self.aspect_ratio = properties.get("specs", {}).get("aspect_ratio", 1.0)
			self.column_span = column_span # Store the intended column span

		def sizeHint(self):
			hint = super().sizeHint()
			preferred_width = int(hint.height() * self.aspect_ratio) # Calculate width based on height and ratio
			return QSize(preferred_width * self.column_span, hint.height()) # Multiply width by column span

		def resizeEvent(self, event):
			super().resizeEvent(event)
			self.adjustSize()

		def _adjust_size(self, size):
			width = size.width()
			height = int(width / self.aspect_ratio)
			return QSize(width, height)

	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Button Grid Test (QPushButton with Aspect Ratio)")
			self.layout = QGridLayout(self)
			self.buttons = {}  # To store the created buttons

			button_ids = list(button_data.keys())
			rows = 9
			columns = 4

			for row in range(rows):
					for column in range(columns):
						index = row * columns + column

						if index < len(button_ids) and button_ids[index] != "equals" and button_ids[index] != "t64_logo": # Skip both for now
							button_id = button_ids[index]
							properties = button_data[button_id]
							# ... (button creation for the main grid remains the same) ...
							button = AspectRatioButton(properties, self)
							if "callback" in properties and properties["callback"]:
									button.clicked.connect(properties["callback"])
							self.layout.addWidget(button, row, column)
							self.buttons[button_id] = button

			# Handle the "t64_logo" button in the last row
			last_row_index = rows
			t64_properties = button_data["t64_logo"]
			t64_button = AspectRatioButton(t64_properties, self)
			t64_button.clicked.connect(t64_properties["callback"])
			self.layout.addWidget(t64_button, last_row_index, 3)
			self.buttons["t64_logo"] = t64_button

			# Handle the "equals" button in the last row, spanning three columns
			equals_properties = button_data["equals"]
			equals_button = AspectRatioButton(equals_properties, self, column_span=3) # Pass column_span
			equals_button.clicked.connect(equals_properties["callback"])
			self.layout.addWidget(equals_button, last_row_index, 0, 1, 3)
			self.buttons["equals"] = equals_button

			self.setLayout(self.layout)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

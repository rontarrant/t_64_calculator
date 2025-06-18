import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)
from callbacks import *

button_data = {
	"numsys_hex":		{"name": "numsys_hex", 		"style": "radio", "group": "numsys",	"state": "inactive",	"callback": select_number_system },
	"digit_d":			{"name": "digit_d", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_d             },
	"digit_e":			{"name": "digit_e", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_e             },
	"digit_f":			{"name": "digit_f", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_f             },
	"t64_logo":			{"name": "t64_logo", 		"style": "perm",  "group": "none",		"state": "always",	"callback": about                },

 	"numsys_dec":		{"name": "numsys_dec", 		"style": "radio", "group": "numsys",	"state": "active",	"callback": select_number_system },
	"digit_a":			{"name": "digit_a", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_a             },
	"digit_b":			{"name": "digit_b", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_b             },
	"digit_c":			{"name": "digit_c", 			"style": "ghost", "group": "none",		"state": "inactive",	"callback": insert_c             },
	"math_div":			{"name": "math_div", 		"style": "perm",  "group": "none",		"state": "always",	"callback": insert_division_sign },

 	"numsys_oct":		{"name": "numsys_oct", 		"style": "radio", "group": "numsys",	"state": "inactive",	"callback": select_number_system },
	"digit_7":			{"name": "digit_7", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_7             },
	"digit_8":			{"name": "digit_8", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_8             },
	"digit_9":			{"name": "digit_9", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_9             },
	"math_mult":		{"name": "math_mult", 		"style": "perm",  "group": "none",		"state": "always",	"callback": insert_multiply_sign },

 	"numsys_bin":		{"name": "numsys_bin", 		"style": "radio", "group": "numsys",	"state": "inactive",	"callback": select_number_system },
	"digit_4":			{"name": "digit_4", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_4             },
	"digit_5":			{"name": "digit_5", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_5             },
	"digit_6":			{"name": "digit_6", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_6             },
	"math_sub":			{"name": "math_sub", 		"style": "perm",  "group": "none",		"state": "always",	"callback": insert_subtract_sign },
 
 	"bit_32":			{"name": "bit_32", 			"style": "radio", "group": "bits",		"state": "inactive",	"callback": select_bit_width     },
	"digit_1":			{"name": "digit_1", 			"style": "perm",  "group": "none",		"state": "always",	"callback": insert_1             },
	"digit_2":			{"name": "digit_2", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_2             },
	"digit_3":			{"name": "digit_3", 			"style": "ghost", "group": "none",		"state": "active",	"callback": insert_3             },
	"math_add":			{"name": "math_add", 		"style": "perm",  "group": "none",		"state": "always",	"callback": insert_addition_sign },

 	"bit_16":			{"name": "bit_16", 			"style": "radio", "group": "bits",		"state": "inactive",	"callback": select_bit_width     },
	"bracket_left":	{"name": "bracket_left", 	"style": "perm",  "group": "none",		"state": "always",	"callback": insert_left_bracket  },
	"digit_0":			{"name": "digit_0", 			"style": "perm",  "group": "none",		"state": "always",	"callback": insert_0             },
	"dot":				{"name": "dot", 				"style": "ghost", "group": "none",		"state": "active",	"callback": insert_dot           },
	"bracket_right":	{"name": "bracket_right", 	"style": "perm",  "group": "none",		"state": "always",	"callback": insert_right_bracket },
 
 	"bit_8":				{"name": "bit_8", 			"style": "radio", "group": "bits",		"state": "active",	"callback": select_bit_width     },
	"signed":			{"name": "signed", 			"style": "perm",  "group": "none",		"state": "inactive",	"callback": set_un_signed        },
	"edit_clear":   	{"name": "edit_clear", 		"style": "perm",  "group": "none",		"state": "always",	"callback": clear_display        },
	"edit_backspace":	{"name": "edit_backspace", "style": "perm",  "group": "none",		"state": "always",	"callback": do_backspace         },
	"math_equals":  	{"name": "math_equals", 	"style": "perm",  "group": "none",		"state": "always",	"callback": do_math              },
} # button_data

if __name__ == "__main__":
	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Button Grid")
			self.layout = QGridLayout(self)
			self.buttons = {}  # To store the created buttons

			button_ids = list(button_data.keys())
			rows = 7
			columns = 5

			for row in range(rows):
				for column in range(columns):
					index = row * columns + column
					if index < len(button_ids):
						button_id = button_ids[index]
						properties = button_data[button_id]
						button_name = properties["name"]
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
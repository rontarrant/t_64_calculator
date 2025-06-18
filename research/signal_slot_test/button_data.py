import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)
from callbacks import *

button_data = {
	"hexadecimal":	{"name": "hexadecimal",	"type": "radio", "group": "numsys",		"default": "inactive",	"callback": select_number_system },
	"digit_d":		{"name": "digit_d", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_d             },
	"digit_e":		{"name": "digit_e", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_e             },
	"digit_f":		{"name": "digit_f", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_f             },
	"t64_logo":		{"name": "t64_logo", 	"type": "perm",  "group": "about",		"default": "active",		"callback": about               	},

 	"decimal":		{"name": "decimal", 		"type": "radio", "group": "numsys",		"default": "active",	"callback": select_number_system 	},
	"digit_a":		{"name": "digit_a", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_a             },
	"digit_b":		{"name": "digit_b", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_b             },
	"digit_c":		{"name": "digit_c", 		"type": "ghost", "group": "hex_digit",	"default": "inactive",	"callback": insert_c             },
	"divide":		{"name": "divide", 		"type": "perm",  "group": "math",		"default": "active",	"callback": insert_division_sign 	},

 	"octal":			{"name": "octal", 		"type": "radio", "group": "numsys",		"default": "inactive",	"callback": select_number_system },
	"digit_7":		{"name": "digit_7", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_7             	},
	"digit_8":		{"name": "digit_8", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_8             	},
	"digit_9":		{"name": "digit_9", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_9             	},
	"multiply":		{"name": "multiply", 	"type": "perm",  "group": "math",		"default": "active",	"callback": insert_multiply_sign 	},

 	"binary":		{"name": "binary", 		"type": "radio", "group": "numsys",		"default": "inactive",	"callback": select_number_system },
	"digit_4":		{"name": "digit_4", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_4             	},
	"digit_5":		{"name": "digit_5", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_5             	},
	"digit_6":		{"name": "digit_6", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_6             	},
	"subtract":		{"name": "subtract", 	"type": "perm",  "group": "math",		"default": "active",	"callback": insert_subtract_sign 	},

  	"bit_32":		{"name": "bit_32", 		"type": "radio", "group": "bits",		"default": "inactive",	"callback": select_bit_width  	},
	"digit_1":		{"name": "digit_1", 		"type": "perm",  "group": "digit",		"default": "active",	"callback": insert_1             	},
	"digit_2":		{"name": "digit_2", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_2             	},
	"digit_3":		{"name": "digit_3", 		"type": "ghost", "group": "dec_digit",	"default": "active",	"callback": insert_3             	},
	"add":			{"name": "add", 			"type": "perm",  "group": "math",		"default": "active",	"callback": insert_addition_sign 	},

 	"bit_16":		{"name": "bit_16", 		"type": "radio", "group": "bits",		"default": "inactive",	"callback": select_bit_width  	},
	"brace_left":	{"name": "brace_left", 	"type": "perm",  "group": "exp_digit",	"default": "active",	"callback": insert_left_bracket  	},
	"digit_0":		{"name": "digit_0", 		"type": "perm",  "group": "digit",		"default": "active",	"callback": insert_0             	},
	"dot":			{"name": "dot", 			"type": "ghost", "group": "dot_digit",	"default": "active",	"callback": insert_dot           	},
	"brace_right":	{"name": "brace_right", "type": "perm",  "group": "exp_digit",	"default": "active",	"callback": insert_right_bracket 	},
 
 	"bit_8":			{"name": "bit_8", 		"type": "radio", "group": "bits",		"default": "active",	"callback": select_bit_width     	},
	"signed":		{"name": "signed", 		"type": "perm",  "group": "sign",		"default": "inactive",	"callback": set_un_signed     	},
	"clear":   		{"name": "clear", 		"type": "perm",  "group": "edit",		"default": "active",	"callback": clear_display        	},

	"and":			{"name": "and",			"type": "perm",  "group": "logic",		"default": "active",	"callback": do_and       				},
	"not":			{"name": "not",			"type": "perm",  "group": "logic",		"default": "active",	"callback": do_not       				},
	"or":				{"name": "or",				"type": "perm",  "group": "logic",		"default": "active",	"callback": do_or       				},
	"xor":			{"name": "xor",			"type": "perm",  "group": "logic",		"default": "active",	"callback": do_xor       				},
	"shift_left":	{"name": "shift_left",	"type": "perm",  "group": "logic",		"default": "active",	"callback": do_shift_left   			},
	"shift_right":	{"name": "shift_right",	"type": "perm",  "group": "logic",		"default": "active",	"callback": do_shift_right				},

	"equals":  		{"name": "equals", 		"type": "perm",  "group": "edit",		"default": "active",	"callback": do_equals              	},
} # button_data

active_radio_buttons = {}
numsys = []
bits = []

groups = ["numsys", "digit", "about", "math", "bits", "sign", "edit"]
states = ["inactive", "active", "active"]
styles = ["radio", "perm", "ghost"]

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
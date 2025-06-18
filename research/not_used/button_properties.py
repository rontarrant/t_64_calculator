import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)
from callbacks import *

button_data = {
	"button_hex":     {"name": "numsys_hex",     "group": "numsys",   "state": "inactive", "callback": select_number_system },
	"button_d":       {"name": "digit_d",        "group": "none",     "state": "inactive", "callback": insert_d             },
	"button_e":       {"name": "digit_e",        "group": "none",     "state": "inactive", "callback": insert_e             },
	"button_f":       {"name": "digit_f",        "group": "none",     "state": "inactive", "callback": insert_f             },
	"button_logo":    {"name": "t64_logo",       "group": "none",     "state": "always",   "callback": about                },

	"button_dec":     {"name": "numsys_dec",     "group": "numsys",   "state": "active",   "callback": select_number_system },
	"button_a":       {"name": "digit_a",        "group": "none",     "state": "inactive", "callback": insert_a             },
	"button_b":       {"name": "digit_b",        "group": "none",     "state": "inactive", "callback": insert_b             },
	"button_c":       {"name": "digit_c",        "group": "none",     "state": "inactive", "callback": insert_c             },
	"button_div":     {"name": "math_div",       "group": "none",     "state": "always",   "callback": insert_division_sign },

	"button_oct":     {"name": "numsys_oct",     "group": "numsys",   "state": "inactive", "callback": select_number_system },
	"button_7":       {"name": "digit_7",        "group": "none",     "state": "active",   "callback": insert_7             },
	"button_8":       {"name": "digit_8",        "group": "none",     "state": "active",   "callback": insert_8             },
	"button_9":       {"name": "digit_9",        "group": "none",     "state": "active",   "callback": insert_9             },
	"button_mult":    {"name": "math_mult",      "group": "none",     "state": "always",   "callback": insert_multiply_sign },

	"button_bin":     {"name": "numsys_bin",     "group": "numsys",   "state": "inactive", "callback": select_number_system },
	"button_4":       {"name": "digit_4",        "group": "none",     "state": "active",   "callback": insert_4             },
	"button_5":       {"name": "digit_5",        "group": "none",     "state": "active",   "callback": insert_5             },
	"button_6":       {"name": "digit_6",        "group": "none",     "state": "active",   "callback": insert_6             },
	"button_sub":     {"name": "math_sub",       "group": "none",     "state": "always",   "callback": insert_subtract_sign },

	"button_bit_32":  {"name": "bit_32",         "group": "bits",     "state": "inactive", "callback": select_bit_width     },
	"button_1":       {"name": "digit_1",        "group": "none",     "state": "always",   "callback": insert_1             },
	"button_2":       {"name": "digit_2",        "group": "none",     "state": "active",   "callback": insert_2             },
	"button_3":       {"name": "digit_3",        "group": "none",     "state": "active",   "callback": insert_3             },
	"button_add":     {"name": "math_add",       "group": "none",     "state": "always",   "callback": insert_addition_sign },

	"button_bit_16":  {"name": "bit_16",         "group": "bits",     "state": "inactive", "callback": select_bit_width     },
	"button_left":    {"name": "bracket_left",   "group": "none",     "state": "always",   "callback": insert_left_bracket  },
	"button_0":       {"name": "digit_0",        "group": "none",     "state": "always",   "callback": insert_0             },
	"button_dot":     {"name": "dot",            "group": "none",     "state": "active",   "callback": insert_dot           },
	"button_right":   {"name": "bracket_right",  "group": "none",     "state": "always",   "callback": insert_right_bracket },

	"button_bit_8":   {"name": "bit_8",          "group": "bits",     "state": "active",   "callback": select_bit_width     },
	"button_signed":  {"name": "signed",         "group": "none",     "state": "inactive", "callback": set_un_signed        },
	"button_clear":   {"name": "edit_clear",     "group": "none",     "state": "always",   "callback": clear_display        },
	"button_back":    {"name": "edit_backspace", "group": "none",     "state": "always",   "callback": do_backspace         },
	"button_equals":  {"name": "math_equals",    "group": "none",     "state": "always",   "callback": do_math              },
} # button_data

groups = {"numsys", "bits"}

if __name__ == '__main__':

	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Button Grid")
			self.layout = QGridLayout(self)
			self.buttons = {}
			self.grouped_buttons = {} # Store buttons by their group

			button_keys = list(button_data.keys())
			rows = 7
			cols = 5

			for row in range(rows):
				for col in range(cols):
					index = row * cols + col
					if index < len(button_keys):
						button_key = button_keys[index]
						data = button_data[button_key]
						button_name = data["name"]
						group = data["group"]
						initial_state = data["state"]
						callback_func = data["callback"]

						button = QPushButton(button_name)
						button.setProperty("button_key", button_key)
						button.setProperty("group", group)
						button.setProperty("state", initial_state)
						button.clicked.connect(self.on_button_clicked)

						self.layout.addWidget(button, row, col)
						self.buttons[button_key] = button

						if group not in self.grouped_buttons:
							self.grouped_buttons[group] = {}
						self.grouped_buttons[group][button_key] = button

						if initial_state == "active" and group in ["numsys", "bits"]:
							self.set_active_button_in_group(group, button_key)

			self.setLayout(self.layout)

		def on_button_clicked(self):
			clicked_button = self.sender()
			if clicked_button is None:
				return

			button_key = clicked_button.property("button_key")
			group = clicked_button.property("group")
			callback_func = button_data[button_key]["callback"]

			if group in ["numsys", "bits"]:
				self.set_active_button_in_group(group, button_key)
			else:
				callback_func()

		def set_active_button_in_group(self, group_name, active_key):
			if group_name not in self.grouped_buttons:
				return

			for key, button in self.grouped_buttons[group_name].items():
				if key == active_key:
					button.setProperty("state", "active")
					# Apply visual style for active state
					self.apply_active_style(button)
					# Call the callback of the newly active button
					#if active_key in button_data:
					#	button_data[active_key]["callback"]()
				else:
					button.setProperty("state", "inactive")
					# Apply visual style for inactive state
					self.apply_inactive_style(button)

		def apply_active_style(self, button):
			# Example: Change background color
			button.setStyleSheet("background-color: lightblue;")

		def apply_inactive_style(self, button):
			# Example: Reset background color
			button.setStyleSheet("") # Or set to a default color

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

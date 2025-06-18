from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QPushButton,
) 

# Assume all support files exist in the same directory
from button_data import *
from c64_palette import C64Palette
from callbacks import *
from analog_buttons import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("T-64 Calculator")
		central_widget = QWidget()
		self.layout = QGridLayout(central_widget)
		self.buttons = {}
		self.numsys_buttons = {}  # New dictionary for number system buttons
		self.bitwidth_buttons = {} # New dictionary for bit width buttons
		self.active_radio_buttons = {"numsys": None, "bits": None} # track mutually-exclusive buttons
		self._create_button_grid() # populate the grid with buttons
		self._update_initial_button_states() # set initial button states
		self.setCentralWidget(central_widget)
		#self.resize(600, 500)

	def _create_button_grid(self):
		button_ids = list(button_data.keys())
		rows = 9
		columns = 4

		for row in range(rows):
			for column in range(columns):
				index = row * columns + column

				if index < len(button_ids):
					button_id = button_ids[index]

					# get properties for the current button
					properties = button_data[button_id]
					button_type = properties["type"]

					# get the button type
					specs = properties["specs"].copy()
					specs.update(properties)

					# build button by type and group
					if button_type == "radio" and properties["group"] == "numsys":
						button = OneLineButton(specs)
						button.clicked.connect(self.handle_numsys_change_wrapper)
						self.numsys_buttons[button_id] = button  # Add to numsys dictionary

						if properties["state"] == "active":
							self.active_radio_buttons["numsys"] = button

					elif button_type == "radio" and properties["group"] == "bits":
						button = TwoLineButton(specs)
						button.clicked.connect(self.handle_bitwidth_change_wrapper)
						self.bitwidth_buttons[button_id] = button # Add to bitwidth dictionary

						if properties["state"] == "active":
							self.active_radio_buttons["bits"] = button

					elif button_type == "hex" and properties["group"] == "digit":
						button = OneLineButton(specs)
					elif button_type == "dec" and properties["group"] == "digit":
						button = OneLineButton(specs)
					elif button_type == "perm" and properties["group"] == "math":
						button = OneLineButton(specs)
					elif button_type == "perm" and properties["group"] == "digit":
						button = OneLineButton(specs)
					elif button_type == "perm" and properties["group"] == "edit":
						button = OneLineButton(specs) # Treat CLR and BS as permanent
					else:
						button = QPushButton(properties["label"]) # Fallback

					if button_type != "radio":
						if "callback" in properties and properties["callback"]:
							button.clicked.connect(lambda checked, window = self, callback = properties["callback"]: callback(window))

					self.layout.addWidget(button, row, column)
					self.buttons[button_id] = button

		# Handle the last row separately (Equals and T-64 Logo)
		equals_properties = button_data["equals"].copy()
		equals_specs = equals_properties["specs"].copy()
		equals_specs.update(equals_properties)
		equals_button = OneLineButton(equals_specs)

		if "callback" in equals_properties and equals_properties["callback"]:
			equals_button.clicked.connect(
				lambda checked, window = self, callback = equals_properties["callback"]: callback(window))

		self.layout.addWidget(equals_button, 9, 0, 1, 3)
		self.buttons["equals"] = equals_button

		t64_properties = button_data["t64_logo"].copy()
		t64_specs = t64_properties["specs"].copy()
		t64_specs.update(t64_properties)
		t64_button = AngledButton(t64_specs)

		if "callback" in t64_properties and t64_properties["callback"]:
			t64_button.clicked.connect(
				lambda checked, window = self, callback = t64_properties["callback"]: callback(window))

		self.layout.addWidget(t64_button, 9, 3)
		self.buttons["t64_logo"] = t64_button

	def handle_numsys_change_wrapper(self):
		from callbacks import handle_numsys_change
		handle_numsys_change(self)

	def handle_bitwidth_change_wrapper(self):
		from callbacks import handle_bitwidth_change
		handle_bitwidth_change(self)

	def _update_initial_button_states(self):
		if self.active_radio_buttons["numsys"]:
			if self.active_radio_buttons["numsys"].properties.get("label") == "BIN":
				self._set_digit_button_states(binary_mode = True)
			elif self.active_radio_buttons["numsys"].properties.get("label") == "DEC":
				self._set_digit_button_states(decimal_mode = True)
			elif self.active_radio_buttons["numsys"].properties.get("label") == "HEX":
				self._set_digit_button_states(hexadecimal_mode = True)
		else:
			# Default to enabling all digits if no numsys is active initially
			self._set_digit_button_states(all_enabled = True)

	def _set_digit_button_states(self, binary_mode = False, decimal_mode = False, hexadecimal_mode = False, all_enabled = False):
		hex_digit_ids = ["a", "b", "c", "d", "e", "f"]
		decimal_digit_ids = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

		for button_id in hex_digit_ids:
			if button_id in self.buttons:
				self.buttons[button_id].setEnabled(hexadecimal_mode or all_enabled)
				self.buttons[button_id].set_active(hexadecimal_mode or all_enabled)
				self.buttons[button_id].update()

		for button_id in decimal_digit_ids:
			if button_id in self.buttons:
				is_enabled = all_enabled
				if binary_mode:
					is_enabled = (button_id == "0" or button_id == "1")
				elif decimal_mode:
					is_enabled = True
				elif hexadecimal_mode:
					is_enabled = True
				self.buttons[button_id].setEnabled(is_enabled)
				self.buttons[button_id].set_active(is_enabled)
				self.buttons[button_id].update()

		if "dot" in self.buttons:
			self.buttons["dot"].set_active(decimal_mode or all_enabled)
			self.buttons["dot"].setEnabled(decimal_mode or all_enabled)
			self.buttons["dot"].update()

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()
	
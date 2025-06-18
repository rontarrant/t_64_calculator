from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QPushButton,
		QLabel
) 

# Assume all support files exist in the same directory
from button_data import *
from c64_palette import C64Palette
from callbacks import *
from analog_buttons import *
from labels import LineEditColourLabel

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("T-64 Calculator")
		screen = QApplication.primaryScreen()
		dpi = screen.logicalDotsPerInch()

		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		
		self.button_layout = QGridLayout(central_widget)
		central_widget.setLayout(self.button_layout)

		# Create input widgets
		self.first_input = LineEditColourLabel(lineedit_properties)
		self.operation_label = QLabel()
		self.second_input = LineEditColourLabel(lineedit_properties)
		self.equals_label = QLabel("=")
		self.results_label = LineEditColourLabel(lineedit_properties)
		self.dummy_widget = QLabel("")

		# Set fonts
		font = QFont()
		font.setPointSize(lineedit_properties["font_size"])
		self.first_input.setFont(font)
		self.second_input.setFont(font)
		self.results_label.setFont(font)
		self.operation_label.setFont(font)
		self.equals_label.setFont(font)
		self.dummy_widget.setFont(font)

		# Let callbacks know about the labels so their text can be manipulated.
		register_labels(self.first_input, self.second_input, self.operation_label, self.results_label)

		# Initialize button dictionaries
		self.buttons = {}
		self.numsys_buttons = {}
		self.bitwidth_buttons = {}
		self.active_radio_buttons = {"numsys": None, "bits": None}

		# Add input widgets to grid (rows 0-2)
		self._create_input_area()
		
		# Create buttons starting from row 3
		self._create_button_grid(start_row = 3)
		
		# Set stretch for all rows and columns
		total_rows = 13  # 3 input rows + 10 button rows
		columns = 4

		for row in range(total_rows):
			self.button_layout.setRowStretch(row, 1)
		for column in range(columns):
			self.button_layout.setColumnStretch(column, 1)

		self.set_initial_size()

		self._update_initial_button_states()
		self.setCentralWidget(central_widget)
		self.first_input.setFocus()

	def _create_input_area(self):
		# Add input widgets to first 3 rows
		size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.first_input.setSizePolicy(size_policy)
		self.button_layout.addWidget(self.first_input, 0, 0, 1, 3)
		self.button_layout.addWidget(self.operation_label, 0, 3)
		
		self.second_input.setSizePolicy(size_policy)
		self.button_layout.addWidget(self.second_input, 1, 0, 1, 3)
		self.button_layout.addWidget(self.equals_label, 1, 3)
		
		self.results_label.setSizePolicy(size_policy)
		self.button_layout.addWidget(self.results_label, 2, 0, 1, 3)
		self.button_layout.addWidget(self.dummy_widget, 2, 3)
		'''
		# Set expanding size policies
		for widget in [self.first_input, self.operation_label, 
							self.second_input, self.equals_label,
							self.results_label, self.dummy_widget]:
			widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		'''

	def _create_button_grid(self, start_row = 0):
		button_ids = list(button_data.keys())
		rows = 9  # button rows - 1 (because the last row is built "by hand")
		columns = 4

		for grid_row in range(rows):
			for column in range(columns):
					absolute_row = start_row + grid_row
					index = grid_row * columns + column
					
					if index < len(button_ids):
						button_id = button_ids[index]
						properties = button_data[button_id].copy()
						specs = properties["specs"].copy()
						specs.update(properties)
						button_type = properties["type"]

						# Create button based on type
						if button_type == "radio" and properties["group"] == "numsys":
							button = OneLineButton(specs)
							button.clicked.connect(self.numsys_button_proxy)
							self.numsys_buttons[button_id] = button

							if properties["state"] == "active":
									self.active_radio_buttons["numsys"] = button

						elif button_type == "radio" and properties["group"] == "bits":
							button = TwoLineButton(specs)
							button.clicked.connect(self.bitwidth_button_proxy)
							self.bitwidth_buttons[button_id] = button

							if properties["state"] == "active":
									self.active_radio_buttons["bits"] = button

						elif button_type in ["hex", "dec"] and properties["group"] == "digit":
							button = OneLineButton(specs)
							button.clicked.connect(self.digit_button_proxy)

						elif button_type == "perm":
							button = OneLineButton(specs)
							if properties["group"] == "math":
									button.clicked.connect(self.math_operation_proxy)
							elif properties["group"] == "digit":
									button.clicked.connect(self.digit_button_proxy)
							elif properties["group"] == "edit":
									button.clicked.connect(self.edit_button_proxy)
							elif properties["group"] == "signed":
									button.clicked.connect(self.signed_button_proxy)
						else:
							button = QPushButton(properties["label"])
							button.clicked.connect(self.signed_button_proxy)

						self.button_layout.addWidget(button, absolute_row, column)
						button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
						self.buttons[button_id] = button

		# Add equals button (row start_row + 9)
		equals_properties = button_data["equals"].copy()
		equals_specs = equals_properties["specs"].copy()
		equals_specs.update(equals_properties)
		equals_button = OneLineButton(equals_specs)
		equals_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		equals_button.clicked.connect(self.equals_proxy)
		self.button_layout.addWidget(equals_button, start_row + 9, 0, 1, 3)
		self.buttons["equals"] = equals_button

		# Add logo button
		t64_properties = button_data["t64_logo"].copy()
		t64_specs = t64_properties["specs"].copy()
		t64_specs.update(t64_properties)
		t64_button = AngledButton(t64_specs)
		t64_button.clicked.connect(self.about_proxy)
		self.button_layout.addWidget(t64_button, start_row + 9, 3)
		self.buttons["t64_logo"] = t64_button

	def set_initial_size(self):
		button_width = base_specs["width"]
		button_height = base_specs["height"]
		input_height = lineedit_properties["height"]
		num_button_rows = 10
		num_button_cols = 4
		spacing = self.button_layout.spacing() # Get the default spacing

		initial_width = num_button_cols * button_width + (num_button_cols - 1) * spacing + margin_pad_x # Add some extra margin
		initial_height = (3 * input_height) + (num_button_rows * button_height) + (num_button_rows - 1 + 2) * spacing + margin_pad_y # Add some extra margin

		self.resize(int(initial_width), int(initial_height))
		self.first_input.setFocus()

	# PROXIES for all buttons
	def signed_button_proxy(self):
		from callbacks import toggle_signed
		toggle_signed(self)
	
	def edit_button_proxy(self):
		from callbacks import edit_operation
		edit_operation(self)
	
	def math_operation_proxy(self):
		from callbacks import set_math_operation
		set_math_operation(self)
	
	def equals_proxy(self):
		from callbacks import do_equals
		do_equals(self)

	def about_proxy(self):
		from callbacks import about
		about(self)

	def digit_button_proxy(self):
		from callbacks import insert_digit
		insert_digit(self)

	def numsys_button_proxy(self):
		from callbacks import handle_numsys_change
		handle_numsys_change(self)

	def bitwidth_button_proxy(self):
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
	
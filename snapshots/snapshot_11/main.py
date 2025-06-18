from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QPushButton,
		QVBoxLayout,  # Import the layout we'll use
		QLineEdit,
		QLabel
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
		screen = QApplication.primaryScreen()
		dpi = screen.logicalDotsPerInch()

		central_widget = QWidget()
		self.main_layout = QVBoxLayout(central_widget) # Use a main vertical layout
		self.input_layout = QGridLayout() # Layout for input widgets
		self.button_layout = QGridLayout() # Rename existing grid layout for clarity

		# Create the new widgets
		self.first_input = QLineEdit()
		self.math_label = QLabel()
		self.second_input = QLineEdit()
		self.equals_label = QLabel("=")
		self.result_widget = QLineEdit()

		# Set a larger font for the QLineEdits (and optionally the QLabels)
		font = QFont()
		font.setPointSize(40)  # Adjust the font size as needed
		self.first_input.setFont(font)
		self.second_input.setFont(font)
		self.result_widget.setFont(font)
		self.math_label.setFont(font)
		self.equals_label.setFont(font)

		# Set style sheets for wider borders
		border_width = "4px"  # Adjust the width as needed
		border_style = "solid"
		border_color = "black"  # You can choose any color
		border_radius = "10px"  # Adjust the radius for more or less rounded corners

		style_sheet = f"border: {border_width} {border_style} {border_color}; border-radius: {border_radius};"
		self.first_input.setStyleSheet(style_sheet)
		self.second_input.setStyleSheet(style_sheet)
		self.result_widget.setStyleSheet(style_sheet)

		# Set a maximum width for the input and result widgets
		max_input_width = 450  # Adjust this value as needed
		self.first_input.setMaximumWidth(max_input_width)
		self.second_input.setMaximumWidth(max_input_width)
		self.result_widget.setMaximumWidth(max_input_width)
	
		self.buttons = {}
		self.numsys_buttons = {}  # New dictionary for number system buttons
		self.bitwidth_buttons = {} # New dictionary for bit width buttons
		self.active_radio_buttons = {"numsys": None, "bits": None} # track mutually-exclusive buttons

		self._create_input_area() # Method to add input widgets to their layout
		self._create_button_grid() # populate the grid with buttons
		self._update_initial_button_states() # set initial button states

		self.main_layout.addLayout(self.input_layout) # Add input layout to the main layout
		self.main_layout.addLayout(self.button_layout) # Add button layout to the main layout

		self.setCentralWidget(central_widget)
		self.first_input.setFocus() # Set initial focus

	def _create_input_area(self):
		self.input_layout.addWidget(self.first_input, 0, 0)      # Row 0, Column 0
		self.input_layout.addWidget(self.math_label, 0, 1)        # Row 0, Column 1

		self.input_layout.addWidget(self.second_input, 1, 0)     # Row 1, Column 0
		self.input_layout.addWidget(self.equals_label, 1, 1)      # Row 1, Column 1

		self.input_layout.addWidget(self.result_widget, 2, 0, 1, 1) # Row 2, Column 0, Span 2 columns

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
					properties = button_data[button_id].copy()
					specs = properties["specs"].copy()
					specs.update(properties)
		
					button_type = properties["type"]

					# get the button type
					specs = properties["specs"].copy()
					specs.update(properties)

					# build button by type and group
					if button_type == "radio" and properties["group"] == "numsys":
						button = OneLineButton(specs)
						button.clicked.connect(self.numsys_button_proxy)
						self.numsys_buttons[button_id] = button  # Add to numsys dictionary

						if properties["state"] == "active":
							self.active_radio_buttons["numsys"] = button

					elif button_type == "radio" and properties["group"] == "bits":
						button = TwoLineButton(specs)
						button.clicked.connect(self.bitwidth_button_proxy)
						self.bitwidth_buttons[button_id] = button # Add to bitwidth dictionary

						if properties["state"] == "active":
							self.active_radio_buttons["bits"] = button

					elif button_type == "hex" and properties["group"] == "digit":
						button = OneLineButton(specs)
						button.clicked.connect(self.digit_button_proxy)
					elif button_type == "dec" and properties["group"] == "digit":
						button = OneLineButton(specs)
						button.clicked.connect(self.digit_button_proxy)
					elif button_type == "perm" and properties["group"] == "math":
						button = OneLineButton(specs)
						button.clicked.connect(self.math_operation_proxy)
					elif button_type == "perm" and properties["group"] == "digit":
						button = OneLineButton(specs)
						button.clicked.connect(self.digit_button_proxy)
					elif button_type == "perm" and properties["group"] == "edit":
						button = OneLineButton(specs) # Treat CLR and BS as permanent
						button.clicked.connect(self.edit_button_proxy)
					elif button_type == "perm" and properties["group"] == "signed":
						button = OneLineButton(specs) # Treat Signed as permanent
						button.clicked.connect(self.signed_button_proxy)
					else:
						button = QPushButton(properties["label"]) # Fallback
						button.clicked.connect(self.signed_button_proxy)

					self.button_layout.addWidget(button, row, column)
					self.buttons[button_id] = button

		# Handle the last row separately because of the oversized Equals button.
		equals_properties = button_data["equals"].copy()
		equals_specs = equals_properties["specs"].copy()
		equals_specs.update(equals_properties)
		equals_button = OneLineButton(equals_specs)
		equals_button.clicked.connect(self.equals_proxy)

		self.button_layout.addWidget(equals_button, 9, 0, 1, 3)
		self.buttons["equals"] = equals_button

		t64_properties = button_data["t64_logo"].copy()
		t64_specs = t64_properties["specs"].copy()
		t64_specs.update(t64_properties)
		t64_button = AngledButton(t64_specs)
		t64_button.clicked.connect(self.about_proxy)

		self.button_layout.addWidget(t64_button, 9, 3)
		self.buttons["t64_logo"] = t64_button

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
	
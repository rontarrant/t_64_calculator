from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QVBoxLayout,
		QPushButton,
) 

from button_data import *
from c64_palette import C64Palette
from callbacks import * # Assuming callbacks.py exists in the same directory
from analog_buttons import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("T-64 Calculator")
		central_widget = QWidget()
		self.layout = QGridLayout(central_widget)
		self.buttons = {}
		self.palette = C64Palette()
		self.active_radio_buttons = {"numsys": None, "bits": None} # To track active radio buttons

		self._create_button_grid()

		self.setCentralWidget(central_widget)
		self.resize(600, 500)

	def _create_button_grid(self):
		button_ids = list(button_data.keys())
		rows = 9
		columns = 4

		for row in range(rows):
			for column in range(columns):
				index = row * columns + column
				if index < len(button_ids):
					button_id = button_ids[index]
					properties = button_data[button_id]
					button_type = properties["type"]
					specs = properties["specs"].copy() # Avoid modifying the original
					palette = properties["palette"] # <--- CORRECTED LINE

					button_properties = specs
					button_properties.update(properties) # Add other properties like label, callback
					button_properties["palette"] = palette

					if button_type == "radio" and properties["group"] == "numsys":
						button = NumberSystemButton(button_properties)
						if properties["state"] == "active":
							self.active_radio_buttons["numsys"] = button
					elif button_type == "radio" and properties["group"] == "bits":
						button = BitWidthButton(button_properties)
						if properties["state"] == "active":
							self.active_radio_buttons["bits"] = button
					elif button_type == "perm" and properties["group"] == "math":
						button = PermanentButton(button_properties)
					elif button_type == "hex" and properties["group"] == "digit":
						button = HexadecimalButton(button_properties)
					elif button_type == "dec" and properties["group"] == "digit":
						button = DecimalButton(button_properties)
					elif button_type == "perm" and properties["group"] == "digit":
						button = PermanentButton(button_properties)
					elif button_type == "perm" and properties["group"] == "edit":
						button = PermanentButton(button_properties) # Treat CLR and BS as permanent
					elif button_type == "perm" and properties["group"] == "about":
						button = AboutButton(button_properties)
					else:
						button = QPushButton(properties["label"]) # Fallback

					if "callback" in properties and properties["callback"]:
						button.clicked.connect(properties["callback"])

					self.layout.addWidget(button, row, column)
					self.buttons[button_id] = button

		# Handle the last row (Equals and T-64 Logo) separately
		equals_properties = button_data["equals"].copy()
		equals_specs = equals_properties["specs"].copy()
		equals_palette = equals_properties["palette"] # <--- CORRECTED LINE
		equals_button_properties = equals_specs
		equals_button_properties.update(equals_properties)
		equals_button_properties["palette"] = equals_palette
		equals_button = PermanentButton(equals_button_properties)
		if "callback" in equals_properties and equals_properties["callback"]:
			equals_button.clicked.connect(equals_properties["callback"])
		self.layout.addWidget(equals_button, 9, 0, 1, 3)
		self.buttons["equals"] = equals_button

		t64_properties = button_data["t64_logo"].copy()
		t64_specs = t64_properties["specs"].copy()
		t64_palette = t64_properties["palette"] # <--- CORRECTED LINE
		t64_button_properties = t64_specs
		t64_button_properties.update(t64_properties)
		t64_button_properties["palette"] = t64_palette
		t64_button = AboutButton(t64_button_properties)
		if "callback" in t64_properties and t64_properties["callback"]:
			t64_button.clicked.connect(t64_properties["callback"])
		self.layout.addWidget(t64_button, 9, 3)
		self.buttons["t64_logo"] = t64_button

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()
	
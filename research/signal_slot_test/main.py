# system imports
import os
import sys

# GUI imports
from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QGridLayout,
)

from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import QPoint, Qt, Signal

# local imports
from button_data import *
from callbacks import *
from calc_buttons import *

image_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/button_images/"

if __name__ == '__main__':
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("Button Grid")
			layout = QGridLayout()

			self.buttons = {}

			button_keys = list(button_data.keys())
			rows = 7
			columns = 5

			# rows = 7
			for row in range(rows):
				# columns = 5
				for column in range(columns):
					# calculate the row and column for each button
					index = row * columns + column
					#print("index: ", index, ", row: ", row, ", column: ", column)

					# keep it within the button_data dictionary (35 keys = 35 buttons)
					if index < len(button_keys):
						# point to the data for the current button
						button_name = button_keys[index]
						data = button_data[button_name] 

						# match button type for instantiation
						# and pass in the path/file for the Button image
						match data["style"]:
							case "perm":
								button = AnalogButton(os.path.join(image_path, button_name), data)
							case "ghost":
								button = GhostableButton(os.path.join(image_path, button_name), data)
							case "radio":
								# set up radio button groups
								match data["group"]:
									case "numsys":
										numsys.append(button_name)
									case "bits":
										bits.append(button_name)
								button = RTRadioButton(os.path.join(image_path, button_name), data)

						layout.addWidget(button, row, column)
						self.buttons[button_name] = button

			central_widget = QWidget()
			central_widget.setLayout(layout)
			self.setCentralWidget(central_widget)

			#print("numsys: ", numsys)
			#print("bits: ", bits)

			# The button that calls this method doesn't matter.
			# This will look through the group and enable the 
			# default set in button_data.py -> active_radio_buttons
			self.buttons["decimal"].enable_default_group_button()

			#for key, value in self.buttons.items():
			#	print(key, " = ", self.buttons[key])



	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
	
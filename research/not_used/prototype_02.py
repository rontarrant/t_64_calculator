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

bits_group = []
numsys_group = []
BUTTON_IMAGE_PATH = path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/button_images/"

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

						# set up radio button groups
						match data["group"]:
							case "numsys":
								numsys_group.append(button_name)
							case "bits":
								bits_group.append(button_name)

						# match button type for instantiation
						# and pass in the path/file for the Button image
						match data["style"]:
							case "perm":
								button = PermanentButton(os.path.join(path, button_name))
							case "ghost":
								button = GhostableButton(os.path.join(path, button_name))
							case "radio":
								button = RTRadioButton(os.path.join(path, button_name))

						layout.addWidget(button, row, column)

						'''
						initial_state = data["state"]
						callback_func = data["callback"]

						button = QPushButton(button_name)
						button.setProperty("button_key", button_name)
						#button.setProperty("group", group)
						button.setProperty("state", initial_state)
						button.clicked.connect(self.on_button_clicked)
						self.buttons[button_name] = button
						'''
						
						#if group in self.grouped_buttons:
						#	self.grouped_buttons[group][button_key] = button

						#if initial_state == "active" and group in groups:
						#	self.set_active_button_in_group(group, button_key)

			central_widget = QWidget()
			central_widget.setLayout(layout)
			self.setCentralWidget(central_widget)

		def on_button_clicked(self):
			clicked_button = self.sender()
			if clicked_button is None:
				return

			button_key = clicked_button.property("button_key")
			group = clicked_button.property("group")
			callback_func = button_data[button_key]["callback"]

			if group in groups:
				self.set_active_button_in_group(group, button_key)
			else:
				callback_func()

		def set_active_button_in_group(self, group_name, active_key):
			if group_name not in self.grouped_buttons:
				return

			for key, button in self.grouped_buttons[group_name].items():
				if key == active_key:
					button.setProperty("state", "active")
					self.apply_active_style(button)
					#if active_key in button_data:
					#	button_data[active_key]["callback"]()
				else:
					button.setProperty("state", "inactive")
					self.apply_inactive_style(button)

		def apply_active_style(self, button):
			button.setStyleSheet("background-color: lightblue;")

		def apply_inactive_style(self, button):
			button.setStyleSheet("")

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
	
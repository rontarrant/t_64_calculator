# system imports
import os
import sys

# GUI imports
from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QHBoxLayout,
)

from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import QPoint, Qt, Signal

# local imports
from button_data import *
from callbacks import *

for button_id, button_info in button_data.items():
	print(f"Button ID: {button_id}") # see list of button names

	for attribute, value in button_info.items():
		print(f"\t{attribute}:", value) # see list of attributes for buttons

	callback = button_data[button_id]['callback']
	group = button_data[button_id]['group']

	match(button_id):
		case 'button_hex' | 'button_dec' | 'button_oct' | 'button_bin':
			#print("Found a number system button")
			callback(button_id, group)
		case 'button_bit_8' | 'button_bit_16' | 'button_bit_32':
			#print("Found a bit width button")
			callback(button_id, group)
		case _:
			#print("Found a DIGIT or MATH button.")
			callback()

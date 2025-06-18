import sys
import os

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QHBoxLayout,
)

from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import QPoint, Qt, Signal

from button_data import *
from callbacks import *


class AnalogButton(QPushButton):
	def __init__(self, image_path, data, parent = None):
		super().__init__(parent)
		self.image = QPixmap(image_path)
		self.pressed_offset = QPoint(5, 5)
		self.current_offset = QPoint(0, 0)
		self.is_pressed = False

		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)
	
	# Override the mousePressEvent to animate the button image.
	# Simulates the down movement of an analog button.
	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		self.is_pressed = True
		self.current_offset = self.pressed_offset
		self.update()

	# This override finishes the animation of the button image.
	# Simulates the up movement of an analog button.
	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		self.is_pressed = False
		self.current_offset = QPoint(0, 0)
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self) # a sort-of overlay to work on
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		if not self.is_pressed: # in 'normal' mode
			shadow_image = self.image.toImage() # copy the image

			# check all pixels in the image and set up the shadow for drawing
			for x in range(shadow_image.width()):
				for y in range(shadow_image.height()):
					# grab the pixel colour
					color = shadow_image.pixelColor(x, y)
					# If there's even a hint of colour...
					if color.alpha() > 0:
						# set transparency to 75%
						alpha = round(color.alpha() * 0.75)
						# set shadow pixel colour as transparent grey
						shadow_image.setPixelColor(x, y, QColor(0, 0, 0, alpha))

			# Draw the shadow.
			painter.setOpacity(0.5) # effectively 37.5% transparency
			painter.drawImage(self.pressed_offset, shadow_image)
			painter.setOpacity(1.0) # reset before drawing the button top

		# Draws the button image over top of the shadow.
		painter.drawPixmap(self.current_offset, self.image)
		painter.end()

class GhostableButton(AnalogButton):
	# Custom signal to indicate enabled/disabled state change
	### Is this necessary? Who needs to know?
	enabled_changed = Signal(bool)

	def __init__(self, image_file_name, data):
		self.active_image_path = image_file_name + ".png"
		self.inactive_image_path = image_file_name + "_inactive.png"
		#print("active_image_path: ", self.active_image_path)
		#print("inactive_image_path: ", self.inactive_image_path)
		super().__init__(self.active_image_path, data)
		self.is_checked = False
		self.setEnabled(True)  # Ensure buttons start enabled
		#self.clicked.connect(self.do_something)
		self.enabled_changed.connect(self.on_enabled_changed)

	def check_enabled_state(self):
		if self.isEnabled() == True:
			print("Enabled")
		else:
			print("Disabled")

	def setEnabled(self, enabled):
		super().setEnabled(enabled)
		self.enabled_changed.emit(enabled)

	def on_enabled_changed(self, enabled):
		if enabled:
			self.replace_image(self.active_image_path)
		else:
			self.replace_image(self.inactive_image_path)

	def replace_image(self, new_image_path):
		self.image = QPixmap(new_image_path)
		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)
		self.update()


class RTRadioButton(AnalogButton):
	### emit a signal indicating group ID and button ID??
	group_id = Signal(str, str)

	def __init__(self, image_file_name, data):
		self.active_image_path = image_file_name + ".png"
		super().__init__(self.active_image_path, data)
		#print("data: ", data)
		self.name = data.get("name")
		self.group = data.get("group")
		self.callback = data.get("callback")
		print("self.name: ", self.name, ", self.group: ", self.group, ", self.callback: ", self.callback)
		self.dependent_buttons = []
		self.clicked.connect(lambda: self.callback(self.group, self.name))

		print("self.name: ", data["name"], "self.group: ", self.group)
		#self.clicked.connect(self.toggle_dependents)
		#self.enabled_changed.connect(self.on_enabled_changed)

	def add_dependents(self, dependent_buttons):
		print("Switching buttons...")
		self.dependent_buttons = dependent_buttons

	def toggle_dependents(self):
		if self.dependent_buttons[0].isEnabled():
			for button in self.dependent_buttons:
				button.setEnabled(False)
				print(button, " disabled")
		else:
			for button in self.dependent_buttons:
				button.setEnabled(True)
				print(button, " enabled")

	def enable_default_group_button(self):
		# enable the default button
		for key, value in active_radio_buttons.items():
			if self.group == key and self.name == value:
				self.setEnabled(True)
			else:
				self.setEnabled(False)

	# This needs to deal with mutual-exclusivity
	def on_enabled_changed(self, enabled):
		# get the button group we're working with
		group = active_radio_buttons[self.group]
		print("button group: ", group)
		if enabled:
			for button in group:
				print("button in group: ", button)
			self.replace_image(self.active_image_path)
			# change all the other buttons in the group to inactive images

		else:
			self.replace_image(self.inactive_image_path)

if __name__ == "__main__":
	image_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/button_images/"

	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("T-64 Calculator")
#
			toggle1_on_image = list(button_data.keys())[2]
			toggle_button1 = GhostableButton(os.path.join(image_path, toggle1_on_image), button_data["digit_d"])

			toggle2_on_image = list(button_data.keys())[3]
			toggle_button2 = GhostableButton(os.path.join(image_path, toggle2_on_image), button_data["digit_e"])

			selector_file_name = list(button_data.keys())[0]
			selector_button = RTRadioButton(os.path.join(image_path, selector_file_name), button_data["hexadecimal"])
			selector_button.add_dependents([toggle_button1, toggle_button2])

			layout = QHBoxLayout()
			layout_widget = QWidget()
			layout_widget.setLayout(layout)
			layout.addWidget(selector_button)
			layout.addWidget(toggle_button1)
			layout.addWidget(toggle_button2)

			toggle_button1.check_enabled_state() # test
			toggle_button2.check_enabled_state() # test
			#toggle_button1.setEnabled(False) # toggle off
			#toggle_button2.setEnabled(False) # toggle off
			toggle_button1.check_enabled_state() # test
			toggle_button2.check_enabled_state() # test

			self.setCentralWidget(layout_widget)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()

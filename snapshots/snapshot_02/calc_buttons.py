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


class PermanentButton(QPushButton):
	def __init__(self, image_path, parent = None):
		super().__init__(parent)
		self.original_image_path = image_path
		self.image = QPixmap(image_path)
		self.pressed_offset = QPoint(5, 5)
		self.current_offset = QPoint(0, 0)
		self.is_pressed = False

		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)

	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		self.is_pressed = True
		self.current_offset = self.pressed_offset
		self.update()

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		self.is_pressed = False
		self.current_offset = QPoint(0, 0)
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		if not self.is_pressed:
			shadow_image = self.image.toImage()

			for x in range(shadow_image.width()):
				for y in range(shadow_image.height()):
					color = shadow_image.pixelColor(x, y)

					if color.alpha() > 0:
						alpha = round(color.alpha() * 0.75)
						shadow_image.setPixelColor(x, y, QColor(0, 0, 0, alpha))

			painter.setOpacity(0.5)
			painter.drawImage(self.pressed_offset, shadow_image)
			painter.setOpacity(1.0)

		painter.drawPixmap(self.current_offset, self.image)
		painter.end()

	def change_image(self, new_image_path):
		self.image = QPixmap(new_image_path)
		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)
		self.update()

class GhostableButton(PermanentButton):
	# Custom signal to indicate enabled/disabled state change
	enabled_changed = Signal(bool)

	def __init__(self, image_file_name):
		self.active_image_path = image_file_name + ".png"
		self.inactive_image_path = image_file_name + "_inactive.png"
		super().__init__(self.active_image_path)
		self.is_checked = False
		self.setEnabled(True)  # Ensure buttons start enabled
		self.clicked.connect(self.do_something)
		self.enabled_changed.connect(self.on_enabled_changed)

	def do_something(self):
		print("Doing Something...")

	def setEnabled(self, enabled):
		super().setEnabled(enabled)
		self.enabled_changed.emit(enabled)

	def on_enabled_changed(self, enabled):
		if enabled:
			self.change_image(self.active_image_path)
		else:
			self.change_image(self.inactive_image_path)


class RTRadioButton(PermanentButton):
	def __init__(self, image_file_name):
		self.active_image_path = image_file_name + ".png"
		super().__init__(self.active_image_path)
		self.clicked.connect(self.toggle_something)
		#self.switch_buttons = switch_buttons

	def set_switch_buttons(self, switch_buttons):
		self.switch_buttons = switch_buttons

	def toggle_something(self):
		if self.switch_buttons[0].isEnabled():
			for button in self.switch_buttons:
				button.setEnabled(False)
				print(button, " disabled")
		else:
			for button in self.switch_buttons:
				button.setEnabled(True)
				print(button, " enabled")


if __name__ == "__main__":
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("T-64 Calculator")
#
			toggle1_on_image = list(button_data.keys())[2]
			toggle1_off_image = toggle1_on_image + "_inactive"
			toggle_button1 = GhostableButton(toggle1_on_image)

			toggle2_on_image = list(button_data.keys())[3]
			toggle2_off_image = toggle2_on_image + "_inactive"
			toggle_button2 = GhostableButton(toggle2_on_image)

			selector_file_name = list(button_data.keys())[0]
			selector_button = RTRadioButton(selector_file_name)
			selector_button.set_switch_buttons([toggle_button1, toggle_button2])

			layout = QHBoxLayout()
			layout_widget = QWidget()
			layout_widget.setLayout(layout)
			layout.addWidget(selector_button)
			layout.addWidget(toggle_button1)
			layout.addWidget(toggle_button2)

			self.setCentralWidget(layout_widget)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()

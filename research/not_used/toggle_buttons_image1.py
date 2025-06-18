import sys

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QHBoxLayout
)

from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import QPoint

from button_data import BUTTON_PATH, button_data

import os

class AnalogButton(QPushButton):
	def __init__(self, image_path, parent=None):
		super().__init__(parent)
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

class ToggleButton(AnalogButton):
	def __init__(self, image_file_name):
		super().__init__(image_file_name)
		self.is_checked = False
		self.setChecked(self.is_checked)
		self.clicked.connect(self.do_something)

	def do_something(self):
		print("Doing Something...")


class PushButton(AnalogButton):
	def __init__(self, image_file_name, toggle_buttons):
		super().__init__(image_file_name)
		self.clicked.connect(self.toggle_something)

		self.toggle_buttons = []

		for toggle_button in toggle_buttons:
			self.toggle_buttons.append(toggle_button)

	def toggle_something(self):
		if self.toggle_buttons[0].isEnabled() == True:
			for button in self.toggle_buttons:
				button.setEnabled(False)
				print(button, " disabled")
		else:
			for button in self.toggle_buttons:
				button.setEnabled(True)
				print(button, " enabled")


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("T-64 Calculator")

		toggle_1_file_name = "digit_e.png"
		toggle_2_file_name = "digit_f.png"
		toggler_file_name = "numsys_dec.png"
		toggle_button1 = ToggleButton(os.path.join(BUTTON_PATH, toggle_1_file_name))
		toggle_button2 = ToggleButton(os.path.join(BUTTON_PATH, toggle_2_file_name))
		
		toggler = PushButton(os.path.join(BUTTON_PATH, toggler_file_name), [toggle_button1, toggle_button2])
		
		layout = QHBoxLayout()
		layout_widget = QWidget()
		layout_widget.setLayout(layout)
		layout.addWidget(toggler)
		layout.addWidget(toggle_button1)
		layout.addWidget(toggle_button2)
		
		self.setCentralWidget(layout_widget)

	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()

# This isn't really the solution to the button width problem,
# but it's as close as any AI has come.
import sys
import os

from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	QPushButton,
	QGridLayout,
	QMainWindow,
)

from PySide6.QtGui import QPainter, QPixmap, QColor, QImage
from PySide6.QtCore import Qt, QPoint

from button_data import BUTTON_PATH, button_data_ordered


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
		print(f"Image Size: {self.image.size()}") #added

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


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = QMainWindow()
	central_widget = QWidget()
	window.setCentralWidget(central_widget)
	window.resize(600,600) #added

	grid_layout = QGridLayout(central_widget)
	grid_layout.setContentsMargins(2, 2, 2, 2)
	grid_layout.setSpacing(2)

	row = 0
	col = 0

	for key in button_data_ordered:
		file_name = button_data_ordered[key][0]
		button = AnalogButton(os.path.join(BUTTON_PATH, file_name))

		grid_layout.addWidget(button, row, col)
		col += 1

		if col >= 5:
			row += 1
			col = 0
		print(f"Button Size: {button.size()}") #added

	window.show()
	sys.exit(app.exec())
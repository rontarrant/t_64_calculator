import sys
import os

from PySide6.QtWidgets import  (
	QApplication,
	QWidget,
	QPushButton,
	QGridLayout,
	QMainWindow,
	QHBoxLayout
)

from PySide6.QtGui import (
	QPainter,
	QPixmap,
	QColor,
	QImage
)

from PySide6.QtCore import (
	Qt,
	QPoint,
	QSize
)

from button_data import (
	BUTTON_PATH,
	button_data_ordered
)

class AnalogButton(QPushButton):
	def __init__(self, image_path, parent = None):
		super().__init__(parent)
		self.image = QPixmap(image_path)
		self.pressed_offset = QPoint(5, 5)
		self.current_offset = QPoint(0, 0)
		self.is_pressed = False

		# Calculate the size correctly
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

		# Draw drop shadow (manual)
		if not self.is_pressed:
			shadow_image = self.image.toImage()
			
			for x in range(shadow_image.width()):
				for y in range(shadow_image.height()):
					color = shadow_image.pixelColor(x, y)
					
					if color.alpha() > 0:
						# set the shadow transparency to 75%
						alpha = round(color.alpha() * .75)
						shadow_image.setPixelColor(x, y, QColor(0, 0, 0, alpha))

			painter.setOpacity(0.5)
			painter.drawImage(self.pressed_offset, shadow_image)
			painter.setOpacity(1.0)

		# Draw image
		painter.drawPixmap(self.current_offset, self.image)

		painter.end()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = QMainWindow()
	central_widget = QWidget()
	window.setCentralWidget(central_widget)
	
	grid_layout = QGridLayout(central_widget)
	grid_layout.setContentsMargins(5, 5, 5, 5)
	grid_layout.setSpacing(2)
	
	row = 0
	col = 0
	
	for key in button_data_ordered:
		file_name = button_data_ordered[key][0]  # Use inactive image
		button = AnalogButton(os.path.join(BUTTON_PATH, file_name))
		
		# Handle equals button spanning two columns
		# It doesn't get the size right, but it's centred.
		# Well, it's a start, anyway.
		if key == "math_equals":
			equals_layout = QHBoxLayout()
			equals_layout.addStretch()  # Left stretch
			equals_layout.addWidget(button)  # Button
			equals_layout.addStretch()  # Right stretch
			
			# Create a placeholder widget for the grid layout
			placeholder_widget = QWidget()
			placeholder_widget.setLayout(equals_layout)
			
			# Add placeholder widget to grid layout
			grid_layout.addWidget(placeholder_widget, row, col, 1, 2)
			col += 2
		else:
			grid_layout.addWidget(button, row, col)
			col += 1
		
		# Advance to next row when column reaches 5
		if col >= 5:
			row += 1
			col = 0
	
	# Ensure the equals button is wide enough to span two columns
	equals_button_index = list(button_data_ordered.keys()).index("math_equals")
	equals_button_row = equals_button_index // 5
	equals_button_col = equals_button_index % 5
	
	# Get the equals button from the layout
	equals_button = grid_layout.itemAtPosition(equals_button_row, equals_button_col).widget()
	
	#window.resize(500, 800)
	window.show()
	sys.exit(app.exec())

import sys
from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QPushButton,
	QSizePolicy,
)

from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPainter, QPainterPath, QPalette

class SmartButton(QPushButton):
	def __init__(self, text="", parent=None, corner_percent=0.25):
		"""
		Create a proportionally rounded button
		:param corner_percent: 0.0 (square) to 0.5 (circle)
		"""
		super().__init__(text, parent)
		self.corner_percent = corner_percent
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		
		# Get current dimensions
		rect = self.rect().adjusted(1, 1, -1, -1)  # Slightly smaller for border
		radius = min(rect.width(), rect.height()) * self.corner_percent
		
		# Create path with proportional rounding
		path = QPainterPath()
		path.addRoundedRect(rect, radius, radius)
		
		# Draw background (changes color when pressed)
		bg_color = self.palette().button().color()
		if self.isDown():
			bg_color = bg_color.darker(120)
		painter.fillPath(path, bg_color)
		
		# Draw text
		painter.drawText(rect, Qt.AlignCenter, self.text())
		
		# Draw border
		border_color = self.palette().shadow().color()
		painter.setPen(border_color)
		painter.drawPath(path)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Proportional Buttons Demo")
		self.setFixedSize(400, 300)
		
		# Set size policy to maintain ratio
		size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		size_policy.setHeightForWidth(True)
		self.setSizePolicy(size_policy)

		central = QWidget()
		self.setCentralWidget(central)
		
		layout = QVBoxLayout(central)
		
		# Row 1 - Different corner percentages
		row1 = QHBoxLayout()
		row1.addWidget(SmartButton("Square (0%)", corner_percent=0.0))
		row1.addWidget(SmartButton("Rounded (15%)", corner_percent=0.15))
		row1.addWidget(SmartButton("Pill (50%)", corner_percent=0.5))
		layout.addLayout(row1)
		
		# Row 2 - Resizable button
		self.resize_button = SmartButton("Resize Me!", corner_percent=0.25)
		layout.addWidget(self.resize_button)
		
		# Row 3 - Vertical expansion test
		row3 = QHBoxLayout()
		row3.addWidget(SmartButton("Tall\nButton", corner_percent=0.2))
		row3.addWidget(SmartButton("Wide Button", corner_percent=0.1))
		layout.addLayout(row3)
		
		# Add stretch to demonstrate button sizing
		layout.addStretch()

	def heightForWidth(self, width):
		"""Calculate height based on width to maintain aspect ratio"""
		return int(width / (4/3))  # 4:3 ratio
	
	def sizeHint(self):
		"""Return preferred size"""
		return QSize(400, 300)
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

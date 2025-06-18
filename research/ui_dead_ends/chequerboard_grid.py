from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import Qt, QRect

class CheckeredGridLayoutWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.grid_layout = QGridLayout(self)
		self.grid_layout.setSpacing(0) # Remove spacing between widgets
		self.color1 = QColor("#f0f0f0")  # Light gray
		self.color2 = QColor("#d3d3d3")  # Darker gray

	def addWidgetToGrid(self, widget, row, col, rowspan=1, colspan=1):
		self.grid_layout.addWidget(widget, row, col, rowspan, colspan)

	def setCellColors(self, color1, color2):
		self.color1 = QColor(color1)
		self.color2 = QColor(color2)
		self.update() # Trigger a repaint

	def paintEvent(self, event):
		painter = QPainter(self)
		rows = self.grid_layout.rowCount()
		columns = self.grid_layout.columnCount()

		for row in range(rows):
			for col in range(columns):
					cell_rect = self.grid_layout.cellRect(row, col)
					painter.fillRect(cell_rect, QBrush(self.color1 if (row + col) % 2 == 0 else self.color2))

		super().paintEvent(event) # Ensure child widgets are painted
		painter.end() # Properly end the painter

if __name__ == "__main__":
	class MainWindow(QWidget):
		def __init__(self):
			super().__init__()
			self.checkered_grid_widget = CheckeredGridLayoutWidget()
			layout = QGridLayout(self)
			layout.addWidget(self.checkered_grid_widget, 0, 0)
			self.setLayout(layout)

			for i in range(4):
					for j in range(4):
						label = QLabel(f"({i}, {j})")
						label.setAlignment(Qt.AlignCenter)
						self.checkered_grid_widget.addWidgetToGrid(label, i, j)

			self.checkered_grid_widget.setCellColors("#e0f2f7", "#b2ebf2") # Light blue and cyan

	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()
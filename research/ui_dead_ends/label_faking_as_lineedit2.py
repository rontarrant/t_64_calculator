import sys
from PySide6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QGridLayout,
	QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

class LineEditLabel(QLabel):
	clicked = Signal()

	def __init__(self, text = ""):
		super().__init__(text)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		self.setFixedHeight(40)

		self.setStyleSheet("""
			background-color: #e0e0e0;
			border: 1px solid #a0a0a0;
			border-radius: 4px;
			padding: 2px;
		""")

		self.setCursor(Qt.CursorShape.IBeamCursor)
		self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enables keyboard focus.
		self.setFocus()  # Automatically focus on initialization.

	def keyPressEvent(self, event: QKeyEvent):
		if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
			self.clearFocus()  # Stops editing when Enter/Return is pressed.
		elif event.key() == Qt.Key.Key_Backspace:
			self.setText(self.text()[:-1])  # Removes the last character.
		else:
			self.setText(self.text() + event.text())  # Appends typed text.

	def mousePressEvent(self, event):
		self.setFocus()  # Ensures the label gains focus on click.

if __name__ == "__main__":
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()
			self.setWindowTitle("4-Column Layout Demo")
			self.setFixedSize(600, 200)
			
			central_widget = QWidget()
			self.setCentralWidget(central_widget)
			layout = QGridLayout(central_widget)
			layout.setSpacing(1)
			layout.setContentsMargins(2, 2, 2, 2)
			
			# Row 0: 3-column button + 4th column button
			wide_button = QPushButton("3-Column Button")

			wide_button.setStyleSheet("background-color: #f0f0f0; border: 1px solid #808080; padding: 5px;")

			layout.addWidget(wide_button, 0, 0, 1, 3)  # Spans cols 0-2
			
			fourth_col_button = QPushButton("Col 3")
			fourth_col_button.setFixedWidth(100)  # Set fixed width for the 4th column button
			layout.addWidget(fourth_col_button, 0, 3)  # In column 3
			
			# Row 1: 3-column label + 4th column label
			three_col_label = LineEditLabel("")
			layout.addWidget(three_col_label, 1, 0, 1, 3)
			three_col_label.setFocus()
			
			fourth_col_label = QLabel("Col 3")
			fourth_col_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			fourth_col_label.setFixedWidth(100)  # Same width as button above
			fourth_col_label.setStyleSheet("""
				background-color: #e0e0e0;
				border: 1px solid #a0a0a0;
				border-radius: 4px;
				padding: 2px;
			""")
			layout.addWidget(fourth_col_label, 1, 3)
			
			# Rows 2-3: Four buttons in each row
			for row in range(2, 4):
				for col in range(4):
						btn = QPushButton(f"Btn {row}-{col}")
						if col == 3:  # Make 4th column buttons same width as above
							btn.setFixedWidth(100)
						else:
							btn.setFixedWidth(80)
						layout.addWidget(btn, row, col)
			
			# Column stretching - first 3 columns expand, 4th stays fixed
			layout.setColumnStretch(0, 1)
			layout.setColumnStretch(1, 1)
			layout.setColumnStretch(2, 1)
			layout.setColumnStretch(3, 0)  # No stretch for fixed-width column

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

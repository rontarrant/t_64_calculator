from PySide6.QtWidgets import QLabel, QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QFocusEvent, QKeyEvent, QFont

class LabelAsLineEdit(QLabel):
	def __init__(self, placeholder_text = "", parent = None):
		super().__init__(parent)
		self.setText(placeholder_text)
		self.setObjectName("LabelAsLineEdit")
		self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.setFont(QFont("Arial", 12))
		self.setStyleSheet("QLabel { border: 1px solid gray; padding: 2px; background: white; }")
		self.setCursor(Qt.CursorShape.IBeamCursor)
		self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
		self._is_editing = False
		self._placeholder_text = placeholder_text

	def mousePressEvent(self, event: QMouseEvent):
		if not self._is_editing:
			self.setFocus()
			self.startEditing()

	def keyPressEvent(self, event: QKeyEvent):
		if self._is_editing:
			if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
					self.stopEditing()
			elif event.key() == Qt.Key.Key_Escape:
					self.stopEditing(cancel = True)
			elif event.key() == Qt.Key.Key_Backspace:
					self.setText(self.text()[:-1])
			else:
					self.setText(self.text() + event.text())

	def focusOutEvent(self, event: QFocusEvent):
		if self._is_editing:
			self.stopEditing()

	def startEditing(self):
		self._is_editing = True
		if self.text() == self._placeholder_text:
			self.setText("")

	def stopEditing(self, cancel=False):
		if cancel or not self.text():
			self.setText(self._placeholder_text)
		self._is_editing = False

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Editable QLabel Example")

		layout = QVBoxLayout(self)
		label_line_edit = LabelAsLineEdit("Click to edit", self)
		layout.addWidget(label_line_edit)

		self.setLayout(layout)

if __name__ == "__main__":
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()

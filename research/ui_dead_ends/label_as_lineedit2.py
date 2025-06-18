from PySide6.QtWidgets import QLabel, QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QFont

class EditableLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName("EditableLabel")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("QLabel { border: 1px solid gray; padding: 2px; background: white; }")
        self.setCursor(Qt.CursorShape.IBeamCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Ensures it can gain focus automatically.
        self.setFocus()  # Automatically focus on the widget.
        self._is_editing = True

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.clearFocus()  # Stops editing on Enter/Return.
        elif event.key() == Qt.Key.Key_Backspace:
            self.setText(self.text()[:-1])  # Handle backspace.
        else:
            self.setText(self.text() + event.text())  # Append typed text.

    def focusOutEvent(self, event):
        self._is_editing = False
        super().focusOutEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editable QLabel Example")

        layout = QVBoxLayout(self)
        editable_label = EditableLabel("", self)
        layout.addWidget(editable_label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

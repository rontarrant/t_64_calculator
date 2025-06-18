# line_edit_colour_label.py (Composition Approach)
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QKeyEvent
from PySide6.QtCore import Qt, QRect, Signal

class CustomColourLabel(QLabel):
    # ... (same CustomColourLabel class as in Approach 1) ...
    pass

class LineEditLabel(QLabel):
    clicked = Signal()

    def __init__(self, text = ""):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.IBeamCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enables keyboard focus.
        self.setFocus()  # Automatically focus on initialization.
        self.default_stylesheet = """
            background-color: transparent;
            border: none;
            padding: 0px;
        """
        self.setStyleSheet(self.default_stylesheet)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.clearFocus()  # Stops editing when Enter/Return is pressed.
        elif event.key() == Qt.Key.Key_Backspace:
            self.setText(self.text()[:-1])  # Removes the last character.
        else:
            self.setText(self.text() + event.text())  # Appends typed text.

    def mousePressEvent(self, event):
        self.setFocus()  # Ensures the label gains focus on click.

class LineEditColourLabel(QWidget):
    def __init__(self, text="", width=200, height=40, corner_radius=4):
        super().__init__()
        self.line_edit = LineEditLabel(text)
        self.colour_label = CustomColourLabel(text, width, height, corner_radius)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.colour_label)
        layout.addWidget(self.line_edit)
        self.line_edit.setAttribute(Qt.WA_TransparentForMouseEvents) # Make line_edit transparent for mouse clicks on colour_label

        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.setLayout(layout)
        self.setFixedSize(width, height)

        # Proxy text changes
        self.line_edit.textChanged.connect(self.colour_label.setText)

    def paintEvent(self, event):
        # The CustomColourLabel handles the painting
        pass

    def focusInEvent(self, event):
        self.line_edit.setFocus()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.line_edit.clearFocus()
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        self.line_edit.keyPressEvent(event)

    def mousePressEvent(self, event):
        self.line_edit.mousePressEvent(event)

    def set_font_size(self, size):
        self.colour_label.set_font_size(size)

    def set_label_size(self, width, height):
        self.width = width
        self.height = height
        self.setFixedSize(width, height)
        self.colour_label.set_label_size(width, height)

    def set_corner_radius(self, radius):
        self.corner_radius = radius
        self.colour_label.set_corner_radius(radius)

    def set_outline_color(self, color):
        self.colour_label.set_outline_color(color)

    def set_text_color(self, color):
        self.colour_label.set_text_color(color)

    def set_background_color(self, color):
        self.colour_label.set_background_color(color)

    def set_outline_width(self, width):
        self.colour_label.set_outline_width(width)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)
        self.colour_label.setText(text)

    def setAlignment(self, alignment):
        self.line_edit.setAlignment(alignment)

    def setSizePolicy(self, hPolicy, vPolicy):
        super().setSizePolicy(hPolicy, vPolicy)
        self.line_edit.setSizePolicy(hPolicy, vPolicy)

    def setFixedWidth(self, width):
        super().setFixedWidth(width)
        self.colour_label.setFixedWidth(width)
        self.line_edit.setFixedWidth(width)

    def setFixedHeight(self, height):
        super().setFixedHeight(height)
        self.colour_label.setFixedHeight(height)
        self.line_edit.setFixedHeight(height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("LineEditColourLabel Demo (Composition)")
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QGridLayout(central_widget)

    label1 = LineEditColourLabel("Type Here", 200, 40, 10)
    layout.addWidget(label1, 0, 0)

    label2 = LineEditColourLabel("Another Field", 250, 50, 15)
    label2.set_background_color(QColor("#f0fff0"))
    label2.set_outline_color(QColor("#008000"))
    label2.set_text_color(QColor("#228b22"))
    label2.set_outline_width(2)
    label2.set_font_size(24)
    layout.addWidget(label2, 1, 0)

    window.show()
    sys.exit(app.exec())

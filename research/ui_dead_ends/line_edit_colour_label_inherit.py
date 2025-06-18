# line_edit_colour_label.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QKeyEvent
from PySide6.QtCore import Qt, QRect, Signal

class CustomColourLabel(QLabel):
    def __init__(self, text, width, height, corner_radius, parent=None):
        super().__init__(text, parent)
        self.outline_color = QColor("#880000")
        self.text_color = QColor("#FF7777")
        self.background_color = QColor("#AAFFEE")
        self.outline_width = 4
        self.font_size = 30  # Default font size
        self.label_width = width
        self.label_height = height
        self.corner_radius = corner_radius
        self.setFixedSize(self.label_width, self.label_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Create a rounded rectangle path
        path = QPainterPath()
        rect = QRect(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

        # 2. Draw the background with rounded corners
        painter.fillPath(path, self.background_color)

        # 3. Draw the outline with rounded corners
        pen = QPen(self.outline_color, self.outline_width)
        painter.setPen(pen)
        painter.drawPath(path)

        # 4. Draw the text, ensuring it's within the rounded rectangle
        font = QFont()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        painter.setPen(self.text_color)
        painter.drawText(rect, Qt.AlignCenter, self.text())

        painter.end()

    def set_font_size(self, size):
        if size > 0:
            self.font_size = size
            self.update()

    def set_label_size(self, width, height):
        if width > 0 and height > 0:
            self.label_width = width
            self.label_height = height
            self.setFixedSize(self.label_width, self.label_height)
            self.update()

    def set_corner_radius(self, radius):
        if radius >= 0:
            self.corner_radius = radius
            self.update()

    def set_outline_color(self, color):
        if isinstance(color, QColor):
            self.outline_color = color
            self.update()

    def set_text_color(self, color):
        if isinstance(color, QColor):
            self.text_color = color
            self.update()

    def set_background_color(self, color):
        if isinstance(color, QColor):
            self.background_color = color
            self.update()

    def set_outline_width(self, width):
        if width >= 0:
            self.outline_width = width
            self.update()

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

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.clearFocus()  # Stops editing when Enter/Return is pressed.
        elif event.key() == Qt.Key.Key_Backspace:
            self.setText(self.text()[:-1])  # Removes the last character.
        else:
            self.setText(self.text() + event.text())  # Appends typed text.

    def mousePressEvent(self, event):
        self.setFocus()  # Ensures the label gains focus on click.

class LineEditColourLabel(LineEditLabel, CustomColourLabel):
    def __init__(self, text="", width=200, height=40, corner_radius=4):
        # Initialize LineEditLabel (which calls QLabel.__init__)
        LineEditLabel.__init__(self, text)
        # Initialize CustomColourLabel with the given dimensions and radius
        CustomColourLabel.__init__(self, text, width, height, corner_radius)
        # Override the default fixed height from LineEditLabel
        self.setFixedHeight(height)
        # Ensure the alignment from LineEditLabel is applied
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def paintEvent(self, event):
        # Call the paintEvent of CustomColourLabel to handle the custom drawing
        CustomColourLabel.paintEvent(self, event)

    # You might want to override or add methods specific to LineEditColourLabel here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("LineEditColourLabel Demo")
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
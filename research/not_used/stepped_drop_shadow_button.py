from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPalette

class ShiftingTopButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._is_pressed = False
        self._button_area_width = 160
        self._button_area_height = 100
        self._top_width = 155
        self._top_height = 95
        self.setFixedSize(self._button_area_width, self._button_area_height)
        self._window_bg_color = self._getWindowBackgroundColor()

    def _getWindowBackgroundColor(self):
        if self.parent():
            palette = self.parent().palette()
            return palette.color(QPalette.Window)
        return QColor("lightgray") # Default if no parent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_pressed = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_pressed = False
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        top_color = QColor("#AAEEFF")
        shadow_color = QColor(0, 0, 0, 80)
        outline_color = text_color = QColor("#0055D4")
        outline_width = 2

        font = painter.font()
        font.setPointSize(16)  # Adjust the font size as needed
        font.setBold(True)  # Make the font bold
        painter.setFont(font)

        # Define rectangles based on the button area
        button_area_rect = self.rect()
        top_size = QSize(self._top_width, self._top_height)

        # Shadow should be in the initial 'covered' position
        shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height),
                            top_size)

        # Button top's position depends on the pressed state
        if not self._is_pressed:
            top_rect = QRect(button_area_rect.topLeft(), top_size)
        else:
            top_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height),
                             top_size)

        # Draw the drop shadow
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(shadow_rect, 5, 5)

        # We are NOT drawing the button area here

        # Draw the button top (fill first)
        painter.setPen(Qt.NoPen) # QPen draws the outline
        painter.setBrush(QBrush(top_color)) # QBrush draws the fill
        painter.drawRoundedRect(top_rect, 5, 5)

        # Draw the brown outline INSIDE the button top
        painter.setPen(QPen(outline_color, outline_width))
        painter.setBrush(Qt.NoBrush) # Important: Don't fill the outline
        painter.drawRoundedRect(top_rect.adjusted(outline_width // 2, outline_width // 2,
                                                  -outline_width // 2, -outline_width // 2), 5, 5)

        # Draw the text on the button top with the new color and size
        painter.setPen(text_color)
        painter.drawText(top_rect, Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shifting Top Button Example")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Set a background color for the window (optional)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("lightgray"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        shifting_button = ShiftingTopButton("Click Me", parent=self) # Ensure parent is set
        layout.addWidget(shifting_button)
        layout.setAlignment(Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
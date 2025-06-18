from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QFontDatabase

class AnalogLookButton(QPushButton):
    def __init__(self, text, font_family="Arial", font_size=16, parent=None):
        super().__init__(text, parent)
        self._is_pressed = False
        self._button_area_width = 160
        self._button_area_height = 100
        self._top_width = 155
        self._top_height = 95
        self.setFixedSize(self._button_area_width, self._button_area_height)
        self._font_family = font_family
        self._font_size = font_size

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

        top_color = QColor("#AAEEFF") # button top: light blue
        shadow_color = QColor(0, 0, 0, 80) # black, 80% transparency
        outline_color = text_color = QColor("#0055D4") # button top outline: dark blue
        outline_width = 4 # width of the button top outline
        text_color = QColor("#0055D4") # text color same as outline

        font = QFont(self._font_family, self._font_size)
        font.setBold(True)
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

        # Draw the text on the button top with the specified font
        painter.setPen(text_color)
        painter.drawText(top_rect, Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shifting Top Button Example")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # You can try different font families available on your system
        font = "Bandwidth Bandless BRK"
        font_size = 25
        #shifting_button = AnalogLookButton("Click Me", font_family = font, font_size = font_size)
        shifting_button = AnalogLookButton("Click Me", font_size = font_size)
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
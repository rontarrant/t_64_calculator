from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class AnalogButton(QPushButton):
    def __init__(self, text, parent = None):
        super().__init__(text, parent)
        
        self._shadow_offset = QPoint(3, 3)
        self._press_offset = QPoint(3, 3)
        self._is_pressed = False

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

        base_color = QColor("lightblue")
        shadow_color = QColor(0, 0, 0, 80)
        border_color = QColor("gray")

        button_rect = self.rect().adjusted(0, 0, -1, -1)
        shadow_rect = button_rect.translated(self._shadow_offset)

        if self._is_pressed:
            button_rect.translate(self._press_offset)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(shadow_rect, 5, 5)

        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(base_color))
        painter.drawRoundedRect(button_rect, 5, 5)

        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(button_rect, Qt.AlignCenter, self.text())

if __name__ == '__main__':
    app = QApplication([])
    main_window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    analog_button = AnalogButton("Click Me")
    analog_button.setMinimumSize(150, 60)  # Give the button some size
    layout.addWidget(analog_button)
    layout.setAlignment(Qt.AlignCenter) # Center the button in the layout

    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    main_window.resize(300, 200)  # Make the window slightly bigger than the button
    main_window.setWindowTitle("Analog Button Example")
    main_window.show()
    app.exec()
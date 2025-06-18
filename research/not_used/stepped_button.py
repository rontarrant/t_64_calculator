from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class SteppedButton(QPushButton):
    def __init__(self, text, top_ratio = 0.7, parent = None):
        super().__init__(text, parent)
        self._top_ratio = max(0.1, min(1.0, top_ratio)) # Ensure ratio is within bounds

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        base_color = QColor("lightgray")
        top_color = QColor("#eee")  # A slightly lighter shade for the top
        border_color = QColor("gray")

        rect = self.rect().adjusted(0, 0, -1, -1) # Inner rect for drawing

        # Calculate the height of the "top" part of the button
        top_height = int(rect.height() * self._top_ratio)
        top_rect = QRect(rect.x(), rect.y(), rect.width(), top_height)
        bottom_rect = QRect(rect.x(), rect.y() + top_height, rect.width(), rect.height() - top_height)

        # Draw the bottom part of the button
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(base_color))
        painter.drawRoundedRect(bottom_rect, 5, 5)

        # Draw the "top" part of the button
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(top_color))
        painter.drawRoundedRect(top_rect, 5, 5)

        # Draw the text on the "top" part
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(top_rect, Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stepped Button Example")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        stepped_button = SteppedButton("Smaller Top", top_ratio=0.6)
        stepped_button.setMinimumSize(150, 60)
        layout.addWidget(stepped_button)
        layout.setAlignment(Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
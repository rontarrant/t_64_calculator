from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QTransform

class AnalogLookButton(QPushButton):
    def __init__(self, button_data, parent = None):
        super().__init__(button_data.get("text", ""), parent)
        self._is_pressed = False
        self._top_width = button_data["width"] - 5
        self._top_height = button_data["height"] - 5
        self.setFixedSize(button_data["width"], button_data["height"])
        self._font_family = button_data.get("font", "Arial")
        self._font_size = button_data.get("font_size", 12)
        self.button_data = button_data

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
        radius = 15

        top_color = self.button_data["top_color"]
        shadow_color = self.button_data["shadow_color"]
        outline_color = self.button_data["outline_color"]
        outline_width = 4
        text_color = self.button_data.get("text_color", QColor("#000000"))

        font = QFont(self._font_family, self._font_size)
        font.setBold(True)
        painter.setFont(font)

        # Define rectangles
        button_area_rect = self.rect()
        top_size = QSize(self._top_width, self._top_height)
        shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
        top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
                         button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

        # Draw shadow, top, and outline
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(shadow_rect, radius, radius)

        painter.setBrush(QBrush(top_color))
        painter.drawRoundedRect(top_rect, radius, radius)

        painter.setPen(QPen(outline_color, outline_width))
        painter.setBrush(Qt.NoBrush)
        area = outline_width // 2
        corner_r = radius - 2
        adjusted_outline = top_rect.adjusted(area, area, -area, -area)
        painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

        # Draw the single line of text
        painter.setPen(text_color)
        painter.drawText(top_rect, Qt.AlignCenter, self.text())

class AngledTextAnalogButton(AnalogLookButton):
    def __init__(self, button_data, parent=None):
        super().__init__(button_data, parent)
        self._angle = button_data.get("text_angle", 0) # Default to 0 degrees

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 15

        top_color = self.button_data["top_color"]
        shadow_color = self.button_data["shadow_color"]
        outline_color = self.button_data["outline_color"]
        outline_width = 4
        text_color = self.button_data.get("text_color", QColor("#000000"))

        font = QFont(self._font_family, self._font_size)
        font.setBold(True)
        painter.setFont(font)

        # Define rectangles
        button_area_rect = self.rect()
        top_size = QSize(self._top_width, self._top_height)
        shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
        top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
                         button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

        # Draw shadow, top, and outline
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(shadow_rect, radius, radius)

        painter.setBrush(QBrush(top_color))
        painter.drawRoundedRect(top_rect, radius, radius)

        painter.setPen(QPen(outline_color, outline_width))
        painter.setBrush(Qt.NoBrush)
        area = outline_width // 2
        corner_r = radius - 2
        adjusted_outline = top_rect.adjusted(area, area, -area, -area)
        painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

        # Prepare for angled text drawing
        painter.save() # Save the current painter state
        painter.setPen(text_color)
        painter.translate(top_rect.center()) # Move origin to the center of the top rect
        painter.rotate(self._angle) # Rotate the coordinate system

        # Calculate the position to draw the text centered after rotation
        text_rect = painter.fontMetrics().boundingRect(self.text())
        text_x = -text_rect.width() / 2
        text_y = -text_rect.height() / 2

        # Draw the angled text
        painter.drawText(int(text_x), int(text_y + painter.fontMetrics().ascent()), self.text())

        # Restore the painter's transformation matrix
        painter.restore()

if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Angled Text Button Example")
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)

            # Single-line button
            button_data_single = {
                "text": "Click!",
                "font": "Arial",
                "font_size": 20,
                "width": 160,
                "height": 100,
                "top_color": QColor("#AAEEFF"),
                "shadow_color": QColor(0, 0, 0, 80),
                "outline_color": QColor("#0055D4"),
                "outline_width": 4,
                "text_color": QColor("#0055D4")
            }
            analog_button = AnalogLookButton(button_data_single)
            layout.addWidget(analog_button)

            # Angled text button
            button_data_angled = {
                "text": "Rotate Me",
                "font": "Helvetica",
                "font_size": 16,
                "width": 180,
                "height": 120,
                "top_color": QColor("#FFEEAA"),
                "shadow_color": QColor(0, 0, 0, 50),
                "outline_color": QColor("#FF8800"),
                "outline_width": 3,
                "text_color": QColor("#FF8800"),
                "text_angle": -30 # Angle in degrees
            }
            angled_button = AngledTextAnalogButton(button_data_angled)
            layout.addWidget(angled_button)

            layout.setAlignment(Qt.AlignCenter)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
            self.resize(350, 250)
            self.show()

    app = QApplication([])
    window = MainWindow()
    app.exec()
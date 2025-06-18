from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont

class AnalogLookButton(QPushButton):
    def __init__(self, button_data, parent = None):
        super().__init__(button_data.get("text", ""), parent) # Provide a default empty string
        self._is_pressed = False
        self._top_width = button_data["width"] - 5
        self._top_height = button_data["height"] - 5
        self.setFixedSize(button_data["width"], button_data["height"])
        self._font_family = button_data.get("font", "Arial") # Provide a default
        self._font_size = button_data.get("font_size", 12) # Provide a default
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

class TwoLineAnalogButton(AnalogLookButton):
    def __init__(self, button_data, parent=None):
        # Call super with dummy text and font info if not present in button_data
        super().__init__({
            "text": button_data.get("text_line1", ""),
            "font": button_data.get("font_line1", "Arial"),
            "font_size": button_data.get("font_size_line1", 12),
            "width": button_data.get("width", 100),
            "height": button_data.get("height", 50),
            "top_color": button_data.get("top_color", QColor("#FFFFFF")),
            "shadow_color": button_data.get("shadow_color", QColor(0, 0, 0, 50)),
            "outline_color": button_data.get("outline_color", QColor("#000000")),
            "outline_width": button_data.get("outline_width", 1),
            "text_color": button_data.get("text_color", QColor("#000000"))
        }, parent)
        self._font_family_line1 = button_data.get("font_line1", self.button_data.get("font", "Arial"))
        self._font_size_line1 = button_data.get("font_size_line1", self.button_data.get("font_size", 12))
        self._text_line1 = button_data.get("text_line1", "")
        self._font_family_line2 = button_data.get("font_line2", self.button_data.get("font", "Arial"))
        self._font_size_line2 = button_data.get("font_size_line2", self.button_data.get("font_size", 12))
        self._text_line2 = button_data.get("text_line2", "")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 15

        top_color = self.button_data["top_color"]
        shadow_color = self.button_data["shadow_color"]
        outline_color = self.button_data["outline_color"]
        outline_width = 4
        text_color = self.button_data.get("text_color", QColor("#000000"))

        # Define rectangles
        button_area_rect = self.rect()
        top_size = QSize(self._top_width, self._top_height)
        shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
        top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
                         button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

        # Draw shadow, top, and outline (reusing logic from AnalogLookButton)
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

        # Draw the two lines of text
        painter.setPen(text_color)

        # Font for the first line
        font_line1 = QFont(self._font_family_line1, self._font_size_line1)
        painter.setFont(font_line1)
        metrics_line1 = painter.fontMetrics()
        text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
        text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2
        text_y_line1 = top_rect.top() + (top_rect.height() / 3) - metrics_line1.descent() / 2

        painter.drawText(int(text_x_line1), int(text_y_line1 + metrics_line1.ascent()), self._text_line1)

        # Font for the second line
        font_line2 = QFont(self._font_family_line2, self._font_size_line2)
        painter.setFont(font_line2)
        metrics_line2 = painter.fontMetrics()
        text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
        text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2
        text_y_line2 = top_rect.bottom() - (top_rect.height() / 3) + metrics_line2.ascent() / 2

        painter.drawText(int(text_x_line2), int(text_y_line2 - metrics_line2.descent()), self._text_line2)

if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Shifting Top Button Example")
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)

            # Data for a single-line button
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

            # Data for a two-line button
            button_data_double = {
                "text_line1": "First",
                "font_line1": "Arial",
                "font_size_line1": 20,
                "text_line2": "Second",
                "font_line2": "Helvetica",
                "font_size_line2": 14,
                "width": 160,
                "height": 100,
                "top_color": QColor("#FFEEAA"),
                "shadow_color": QColor(0, 0, 0, 50),
                "outline_color": QColor("#FF8800"),
                "outline_width": 3,
                "text_color": QColor("#FF8800")
            }
            # Ensure 'text', 'font', and 'font_size' are present for the super().__init__ call
            if "text" not in button_data_double:
                button_data_double["text"] = button_data_double.get("text_line1", "")
            if "font" not in button_data_double:
                button_data_double["font"] = button_data_double.get("font_line1", "Arial")
            if "font_size" not in button_data_double:
                button_data_double["font_size"] = button_data_double.get("font_size_line1", 12)

            two_line_button = TwoLineAnalogButton(button_data_double)
            layout.addWidget(two_line_button)

            layout.setAlignment(Qt.AlignCenter)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
            self.resize(300, 250)
            self.show()

    app = QApplication([])
    window = MainWindow()
    app.exec()
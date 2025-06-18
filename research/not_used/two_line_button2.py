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
        button_data_line1 = button_data.get("line1", {})
        super().__init__(button_data_line1, parent)

        self._font_family_line1 = button_data_line1.get("font", "Arial")
        self._font_size_line1 = button_data_line1.get("font_size", 12)
        self._text_line1 = button_data_line1.get("text", "")

        button_data_line2 = button_data.get("line2", {})
        self._font_family_line2 = button_data_line2.get("font", "Arial")
        self._font_size_line2 = button_data_line2.get("font_size", 12)
        self._text_line2 = button_data_line2.get("text", "")

        # Override width and height based on the first line's data (assuming both lines should fit within the same button size)
        self._top_width = button_data_line1.get("width", 100) - 5
        self._top_height = button_data_line1.get("height", 50) - 5
        self.setFixedSize(button_data_line1.get("width", 100), button_data_line1.get("height", 50))

        # We'll still store the full button_data for potential access in paintEvent if needed
        self.button_data = button_data

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 15

        top_color = self.button_data.get("line1", {}).get("top_color", QColor("#FFFFFF"))
        shadow_color = self.button_data.get("line1", {}).get("shadow_color", QColor(0, 0, 0, 50))
        outline_color = self.button_data.get("line1", {}).get("outline_color", QColor("#000000"))
        outline_width = self.button_data.get("line1", {}).get("outline_width", 4)
        text_color = self.button_data.get("line1", {}).get("text_color", QColor("#000000"))

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

        # Draw the two lines of text
        painter.setPen(text_color)

        # Font for the first line
        font_line1 = QFont(self._font_family_line1, self._font_size_line1)
        painter.setFont(font_line1)
        metrics_line1 = painter.fontMetrics()
        text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
        text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2
        line1_height = metrics_line1.height()

        # Calculate the vertical baseline for the first line
        line1_baseline_y = top_rect.top() + (top_rect.height() / 2) # Adjust the /3 for initial position
        painter.drawText(int(text_x_line1), int(line1_baseline_y), self._text_line1)

        # Font for the second line
        font_line2 = QFont(self._font_family_line2, self._font_size_line2)
        painter.setFont(font_line2)
        metrics_line2 = painter.fontMetrics()
        text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
        text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2  # Define text_x_line2 here
        line2_height = metrics_line2.height()

        # Calculate the vertical baseline for the second line
        line2_baseline_y = top_rect.bottom() - (top_rect.height() / 4) # Adjust the /4 for initial position
        painter.drawText(int(text_x_line2), int(line2_baseline_y), self._text_line2)

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

            # Data for a two-line button (now with two complete sub-dictionaries)
            button_data_double = {
                "line1": {
                    "text": "First Line",
                    "font": "Arial",
                    "font_size": 20,
                    "width": 160,
                    "height": 100,
                    "top_color": QColor("#FFEEAA"),
                    "shadow_color": QColor(0, 0, 0, 80),
                    "outline_color": QColor("#FF8800"),
                    "outline_width": 3,
                    "text_color": QColor("#FF8800")
                },
                "line2": {
                    "text": "Second Line",
                    "font": "Helvetica",
                    "font_size": 14,
                    "text_color": QColor("#007700") # Different text color for the second line
                    # Note: Other properties like width, height, colors for the second line are ignored for the base button drawing
                }
            }
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
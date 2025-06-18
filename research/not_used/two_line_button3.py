from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont

class AnalogButton(QPushButton):
    def __init__(self, button_data, text_data = None, parent = None):
        text = text_data.get("text", "") if text_data else button_data.get("text", "")
        super().__init__(text, parent)
        self._is_pressed = False
        self._top_width = button_data.get("width", 100) - 5
        self._top_height = button_data.get("height", 50) - 5
        self.setFixedSize(button_data.get("width", 100), button_data.get("height", 50))
        self.button_data = button_data
        self.text_data = text_data if text_data else {
            "text": button_data.get("text", ""),
            "font": button_data.get("font", "Arial"),
            "font_size": button_data.get("font_size", 12),
            "color": button_data.get("text_color", QColor("#000000"))
        }

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

        top_color = self.button_data.get("top_color", QColor("#FFFFFF"))
        shadow_color = self.button_data.get("shadow_color", QColor(0, 0, 0, 50))
        outline_color = self.button_data.get("outline_color", QColor("#000000"))
        outline_width = self.button_data.get("outline_width", 4)
        text_color = self.text_data.get("color", QColor("#000000"))
        font_family = self.text_data.get("font", "Arial")
        font_size = self.text_data.get("font_size", 12)
        text = self.text_data.get("text", "")

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
        painter.setFont(QFont(font_family, font_size))
        painter.drawText(top_rect, Qt.AlignCenter, text)

class AngledTextAnalogButton(AnalogButton):
    def __init__(self, button_data, text_data, parent = None):
        super().__init__(button_data, text_data, parent)
        self._angle = text_data.get("text_angle", 0) # Default to 0 degrees
        self._font_family = self.text_data.get("font", "Arial")
        self._font_size = self.text_data.get("font_size", 12)
        self._text = self.text_data.get("text", "")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 15

        top_color = self.button_data["top_color"]
        shadow_color = self.button_data["shadow_color"]
        outline_color = self.button_data["outline_color"]
        outline_width = 4
        text_color = self.text_data.get("text_color", QColor("#000000"))

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

class TwoLineAnalogButton(AnalogButton):
    def __init__(self, button_data, text_data, parent=None):
        super().__init__(button_data, text_data.get("line1"), parent)

        self.text_data_line1 = text_data.get("line1", {})
        self.text_data_line2 = text_data.get("line2", {})

        self._font_family_line1 = self.text_data_line1.get("font", "Arial")
        self._font_size_line1 = self.text_data_line1.get("font_size", 12)
        self._text_line1 = self.text_data_line1.get("text", "")

        self._font_family_line2 = self.text_data_line2.get("font", "Arial")
        self._font_size_line2 = self.text_data_line2.get("font_size", 12)
        self._text_line2 = self.text_data_line2.get("text", "")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 15

        top_color = self.button_data.get("top_color", QColor("#FFFFFF"))
        shadow_color = self.button_data.get("shadow_color", QColor(0, 0, 0, 50))
        outline_color = self.button_data.get("outline_color", QColor("#000000"))
        outline_width = self.button_data.get("outline_width", 4)
        text_color_line1 = self.text_data_line1.get("text_color", self.text_data.get("color", QColor("#000000")))
        text_color_line2 = self.text_data_line2.get("text_color", QColor("#000000"))

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
        # Font for the first line
        font_line1 = QFont(self._font_family_line1, self._font_size_line1)
        painter.setFont(font_line1)
        metrics_line1 = painter.fontMetrics()
        text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
        text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2

        # Calculate the vertical baseline for the first line
        line1_baseline_y = top_rect.top() + (top_rect.height() / 2)
        painter.setPen(text_color_line1)
        painter.drawText(int(text_x_line1), int(line1_baseline_y), self._text_line1)

        # Font for the second line
        font_line2 = QFont(self._font_family_line2, self._font_size_line2)
        painter.setFont(font_line2)
        metrics_line2 = painter.fontMetrics()
        text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
        text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2

        # Calculate the vertical baseline for the second line
        line2_baseline_y = top_rect.bottom() - (top_rect.height() / 4)
        painter.setPen(text_color_line2)
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
                    "width": 160,
                    "height": 100,
                    "top_color": QColor("#AAEEFF"),
                    "shadow_color": QColor(0, 0, 0, 80),
                    "outline_color": QColor("#0055D4"),
                    "outline_width": 4,
            }
            text_data_single = {
                    "text": "Click!",
                    "font": "Arial",
                    "font_size": 20,
                    "color": QColor("#0055D4")
            }
            analog_button = AnalogButton(button_data_single, text_data_single)
            layout.addWidget(analog_button)

            # Data for a two-line button
            button_data = {
                    "width": 160,
                    "height": 100,
                    "top_color": QColor("#FFEEAA"),
                    "shadow_color": QColor(0, 0, 0, 50),
                    "outline_color": QColor("#FF8800"),
                    "outline_width": 3,
            }
            button_two_line_text_data = {
                    "line1": {
                        "text": "First Line",
                        "font": "Arial",
                        "font_size": 20,
                        "text_color": QColor("#FF8800")
                    },
                    "line2": {
                        "text": "Second Line",
                        "font": "Helvetica",
                        "font_size": 14,
                        "text_color": QColor("#007700")
                    }
            }
            two_line_button = TwoLineAnalogButton(button_data, button_two_line_text_data)
            layout.addWidget(two_line_button)

            # Angled text button
            button_data_angled = {
                "width": 180,
                "height": 120,
                "top_color": QColor("#FFEEAA"),
                "shadow_color": QColor(0, 0, 0, 50),
                "outline_color": QColor("#FF8800"),
                "outline_width": 3,
            }
            text_data_angled = {
                "text": "Rotate Me",
                "font": "Helvetica",
                "font_size": 16,
                "text_color": QColor("#FF8800"),
                "text_angle": -30 # Angle in degrees
            }

            angled_button = AngledTextAnalogButton(button_data_angled, text_data_angled)
            layout.addWidget(angled_button)

            layout.setAlignment(Qt.AlignCenter)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
            self.resize(300, 250)
            self.show()
        
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
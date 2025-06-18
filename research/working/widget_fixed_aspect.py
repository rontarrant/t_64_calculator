import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSizePolicy

class AspectWidget(QWidget):
    '''
    A widget that maintains its aspect ratio.
    '''
    def __init__(self, *args, ratio = 16/9, **kwargs):
        super().__init__(*args, **kwargs)
        self.ratio = ratio
        self.adjusted_to_size = (-1, -1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))

    def resizeEvent(self, event):
        size = event.size()
        if size == self.adjusted_to_size:
            return
        self.adjusted_to_size = size

        full_width = size.width()
        full_height = size.height()
        width = min(full_width, full_height * self.ratio)
        height = min(full_height, full_width / self.ratio)

        h_margin = round((full_width - width) / 2)
        v_margin = round((full_height - height) / 2)

        self.setContentsMargins(h_margin, v_margin, h_margin, v_margin)

class AspectRatioButton(QWidget):
    def __init__(self, text, aspect_ratio=1.0, parent=None):
        super().__init__(parent)
        self.aspect_widget = AspectWidget(ratio=aspect_ratio)
        self.button = QPushButton(text)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self.aspect_widget)
        layout.addWidget(self.button)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins within AspectWidget

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.aspect_widget)
        self.setLayout(main_layout)

    def clicked(self):
        return self.button.clicked

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Example 1: Square button (aspect ratio 1:1)
    square_button = AspectRatioButton("Square", aspect_ratio=1.0)

    # Example 2: Wider button (aspect ratio 2:1)
    wide_button = AspectRatioButton("Wide", aspect_ratio=2.0)

    # Example 3: Taller button (aspect ratio 1:2)
    tall_button = AspectRatioButton("Tall", aspect_ratio=1.0/2.0)

    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(square_button)
    layout.addWidget(wide_button)
    layout.addWidget(tall_button)
    window.setLayout(layout)
    window.setWindowTitle("Aspect Ratio Buttons")
    window.show()

    sys.exit(app.exec())
import sys
from resizable import *
#from mixin_class import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout(window)

    button = AnalogButton("Resizable Button", initial_font_size=10, font_factor=0.4)
    line_edit = ResizableLineEdit("Resizable LineEdit", initial_font_size=14, font_factor=0.6)

    layout.addWidget(button)
    layout.addWidget(line_edit)

    window.setWindowTitle("Resizable Widgets Demo")
    window.resize(300, 200) # Set an initial size for the window
    window.show()

    sys.exit(app.exec())

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton
from PySide6.QtGui import QIcon
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

radio_button1 = QRadioButton("Image Option 1")
radio_button2 = QRadioButton("Image Option 2")

stylesheet = """
QRadioButton::indicator {
    width: 0px;
    height: 0px;
}

QRadioButton::indicator:unchecked {
    image: url(button_images/numsys_dec.png); /* Replace with actual path to UNCHECKED image */
}

QRadioButton::indicator:checked {
    image: url(button_images/numsys_dec_inactive.png);   /* Replace with actual path to CHECKED image */
}

QRadioButton {
    spacing: 5px; /* Adjust spacing between image and text if you still have text */
}
"""

window.setStyleSheet(stylesheet)

layout.addWidget(radio_button1)
layout.addWidget(radio_button2)
window.setLayout(layout)
window.show()
sys.exit(app.exec())
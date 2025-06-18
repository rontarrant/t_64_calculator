from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PySide6.QtGui import QFont, QFontDatabase
import sys
import os

def main():
    app = QApplication(sys.argv)

    # Create a directory named 'fonts' in the same directory as your script
    fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
    os.makedirs(fonts_dir, exist_ok=True)

    # Assuming you have a font file named 'my_custom_font.ttf' in the 'fonts' directory
    font_path = os.path.join(fonts_dir, "bandless.ttf")

    # Load the font file
    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            custom_font_family = font_families[0]
            print(f"Loaded font family: {custom_font_family}")

            # Create a QPushButton
            button = QPushButton("Custom Font Button")

            # Create a QFont object with the loaded font family and a size
            custom_font = QFont(custom_font_family, 16)
            button.setFont(custom_font)

            # Basic layout to show the button
            window = QWidget()
            layout = QVBoxLayout(window)
            layout.addWidget(button)
            window.setLayout(layout)
            window.show()

            sys.exit(app.exec())
        else:
            print("Error: Could not get font family name.")
    else:
        print(f"Error: Could not load font file: {font_path}. Make sure the file exists.")

if __name__ == '__main__':
    main()
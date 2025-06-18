from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect

class GridBorderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0) # Remove spacing between widgets

    def addWidgetToGrid(self, widget, row, col, rowspan=1, colspan=1):
        self.grid_layout.addWidget(widget, row, col, rowspan, colspan)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine) # Black, 1-pixel solid line
        painter.setPen(pen)

        layout = self.grid_layout
        rows = layout.rowCount()
        columns = layout.columnCount()

        # Draw horizontal lines
        y = 0
        for r in range(rows + 1):
            line_y = self.mapToGlobal(layout.cellRect(r, 0).topLeft()).y() - self.mapToGlobal(self.rect().topLeft()).y() if r < rows else self.height()
            painter.drawLine(0, y, self.width(), y)
            if r < rows:
                y = line_y + layout.cellRect(r, 0).height() - (layout.spacing() if r < rows -1 else 0)


        # Draw vertical lines
        x = 0
        for c in range(columns + 1):
            line_x = self.mapToGlobal(layout.cellRect(0, c).topLeft()).x() - self.mapToGlobal(self.rect().topLeft()).x() if c < columns else self.width()
            painter.drawLine(x, 0, x, self.height())
            if c < columns:
                x = line_x + layout.cellRect(0, c).width() - (layout.spacing() if c < columns - 1 else 0)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_border_widget = GridBorderWidget()
        layout = QGridLayout(self)
        layout.addWidget(self.grid_border_widget, 0, 0)
        self.setLayout(layout)

        label1 = QLabel("Item 1")
        label2 = QLabel("Item 2")
        label3 = QLabel("Item 3")
        label4 = QLabel("Item 4")

        self.grid_border_widget.addWidgetToGrid(label1, 0, 0)
        self.grid_border_widget.addWidgetToGrid(label2, 0, 1)
        self.grid_border_widget.addWidgetToGrid(label3, 1, 0)
        self.grid_border_widget.addWidgetToGrid(label4, 1, 1)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

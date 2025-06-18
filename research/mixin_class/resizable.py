from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QApplication, QVBoxLayout
from PySide6.QtCore import QSize

from mixin_class import *

# --- Assume FontResizingMixin is defined as above ---

class AnalogButton(FontResizingMixin, QPushButton):
    def __init__(self, text, initial_font_size=12, font_factor=0.5, parent=None):
        # --- IMPORTANT: Call order matters ---
        # 1. Call the primary base class (QPushButton) __init__
        QPushButton.__init__(self, text, parent)
        # 2. Initialize the mixin features
        self._init_font_resizing(initial_font_size, font_factor)

    def resizeEvent(self, event):
        # 1. Call the primary base class's resizeEvent FIRST
        QPushButton.resizeEvent(self, event)
        # super().resizeEvent(event) # This would also work due to MRO

        # 2. Perform font adjustment logic from the mixin
        # Only start adjusting *after* the first resize event completes
        if self._is_ready_for_font_adjust:
            self.adjust_font_size()
        else:
            # Mark ready after the first event processing
            self._mark_ready_for_adjust()


    def sizeHint(self):
        # Provide a default size specific to this button type
        return QSize(100, 60)

from PySide6.QtWidgets import QLineEdit # Other imports as before
from PySide6.QtCore import QSize      # Other imports as before
# Assume FontResizingMixin is defined as before

class ResizableLineEdit(FontResizingMixin, QLineEdit):
    def __init__(self, initial_text="", initial_font_size=12, font_factor=0.7, parent=None):
        # 1. Init the base QLineEdit
        QLineEdit.__init__(self, initial_text, parent)

        # 2. Init the font resizing (this sets the initial font)
        self._init_font_resizing(initial_font_size, font_factor)

        # --- Fix Start ---
        # 3. Store the size hints based on the INITIAL font size *after* it's set
        # We use super() to get the QLineEdit's default calculation for the initial state.
        self._initial_size_hint = super().sizeHint()
        self._initial_min_size_hint = super().minimumSizeHint()
        # --- Fix End ---


    def resizeEvent(self, event):
        # 1. Call base resizeEvent
        QLineEdit.resizeEvent(self, event)
        # super().resizeEvent(event) # Or use super

        # 2. Adjust font if ready
        if self._is_ready_for_font_adjust:
            self.adjust_font_size()
        else:
            # Mark ready after the first layout pass
            self._mark_ready_for_adjust()

    # --- Fix Start ---
    # Override sizeHint and minimumSizeHint to return the *stored* initial hints.
    # This prevents the widget from demanding more space just because the font grew internally.
    def sizeHint(self):
        # If you want some padding you could add it here, but return based on initial
        # return self._initial_size_hint.grownBy(QMargins(5,2,5,2)) # Example padding
        return self._initial_size_hint

    def minimumSizeHint(self):
        # This is often the most important one for stopping layout feedback loops.
        return self._initial_min_size_hint
    # --- Fix End ---

    # Optional: You might still want the specific adjust_font_size override
    # if the mixin's default (based on min(width, height)) isn't ideal for a line edit.
    # (See previous answer for example override)
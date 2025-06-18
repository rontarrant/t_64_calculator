from PySide6.QtGui import QFont
from PySide6.QtCore import QSize # Import QSize if needed elsewhere, though not directly used in Mixin

class FontResizingMixin:
    """
    A mixin class providing font size adjustment based on widget size.

    Requires the inheriting class to also inherit from QWidget (or a subclass)
    and call _init_font_resizing in its __init__ and integrate
    adjust_font_size into its resizeEvent.
    """
    def _init_font_resizing(self, initial_font_size=12, font_factor=0.5):
        # Store configuration
        self._initial_font_size = initial_font_size
        self._font_factor = font_factor # Renamed for clarity
        self._current_font_size = initial_font_size
        self._is_ready_for_font_adjust = False # Flag to wait for first real resize

        # Set the initial font on the widget ('self' will be the actual widget instance)
        try:
            font = self.font()
            font.setPointSize(self._initial_font_size)
            self.setFont(font)
            # print(f"Mixin Initial font size set to: {self._initial_font_size}")
        except AttributeError as e:
            print(f"Error: FontResizingMixin must be used with a QWidget subclass. {e}")

    def _mark_ready_for_adjust(self):
        """Call this after the first resize event processing."""
        self._is_ready_for_font_adjust = True

    def adjust_font_size(self):
        """Adjusts the widget's font size based on its current dimensions."""
        if not hasattr(self, 'width') or not hasattr(self, 'height'):
            # Ensure we're mixed in with something that has dimensions
            return

        widget_width = self.width()
        widget_height = self.height()

        # --- Potential Customization Point ---
        # Decide how to calculate available space.
        # For square-ish things like buttons, min(width, height) is good.
        # For a QLineEdit, maybe height is more important?
        # You could make this calculation strategy configurable if needed.
        available_space = min(widget_width, widget_height)
        # Example alternative for LineEdit: available_space = widget_height * 0.9 # Use 90% of height

        new_font_size = int(available_space * self._font_factor)

        # Apply minimum font size
        min_font_size = 6
        if new_font_size < min_font_size:
            new_font_size = min_font_size

        # Update font only if the size has actually changed
        if new_font_size != self._current_font_size:
            try:
                font = self.font()
                font.setPointSize(new_font_size)
                self.setFont(font)
                self._current_font_size = new_font_size
                # print(f"Font size adjusted to: {new_font_size}")
            except AttributeError as e:
                 print(f"Error: FontResizingMixin could not set font. {e}")

    # Note: sizeHint is specific to the widget, so it stays out of the mixin.
    # The resizeEvent handling is also delegated to the inheriting class
    # to ensure proper superclass calls.
    
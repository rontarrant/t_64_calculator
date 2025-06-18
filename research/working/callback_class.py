from typing import Callable, Dict, Any

from callbacks import *

class ButtonCallbacks:
    """
    A class to hold and manage button callback functions.

    This class provides a structured way to store and access callback
    functions associated with different button actions. It also allows
    for easy extension and modification of the callback functions.
    """

    def __init__(self):
        """Initializes the ButtonCallbacks with empty callback dictionaries."""
        self.callbacks: Dict[str, Callable[..., Any]] = {}
        self.button_groups: Dict[str, list[str]] = {}
        self.initialize_callbacks()

    def initialize_callbacks(self):
        """
        Initializes the callback functions.

        This method defines and stores the callback functions in the
        `callbacks` dictionary. Each key in the dictionary represents a
        specific button action, and the value is the corresponding
        callback function.
        """
        self.callbacks["insert_0"] = insert_0
        self.callbacks["insert_1"] = insert_1
        self.callbacks["insert_2"] = insert_2
        self.callbacks["insert_3"] = insert_3
        self.callbacks["insert_4"] = insert_4
        self.callbacks["insert_5"] = insert_5
        self.callbacks["insert_6"] = insert_6
        self.callbacks["insert_7"] = insert_7
        self.callbacks["insert_8"] = insert_8
        self.callbacks["insert_9"] = insert_9
        self.callbacks["insert_a"] = insert_a
        self.callbacks["insert_b"] = insert_b
        self.callbacks["insert_c"] = insert_c
        self.callbacks["insert_d"] = insert_d
        self.callbacks["insert_e"] = insert_e
        self.callbacks["insert_f"] = insert_f
        self.callbacks["about"] = about
        self.callbacks["select_number_system"] = select_number_system
        self.callbacks["select_bit_width"] = select_bit_width
        self.callbacks["set_un_signed"] = set_un_signed
        self.callbacks["insert_division_sign"] = insert_division_sign
        self.callbacks["insert_multiply_sign"] = insert_multiply_sign
        self.callbacks["insert_subtract_sign"] = insert_subtract_sign
        self.callbacks["insert_addition_sign"] = insert_addition_sign
        self.callbacks["insert_dot"] = insert_dot
        self.callbacks["insert_left_bracket"] = insert_left_bracket
        self.callbacks["insert_right_bracket"] = insert_right_bracket
        self.callbacks["clear_display"] = clear_display
        self.callbacks["do_backspace"] = do_backspace
        self.callbacks["do_math"] = do_math
        # Define button groups
        self.button_groups["numsys"] = ["numsys_hex", "numsys_dec", "numsys_oct", "numsys_bin"]
        self.button_groups["bits"] = ["bit_8", "bit_16", "bit_32"]

    def get_callback(self, callback_name: str) -> Callable[..., Any] | None:
        """
        Retrieves a callback function by its name.

        Args:
            callback_name (str): The name of the callback function to retrieve.

        Returns:
            Callable[..., Any] | None: The callback function if found, otherwise None.
        """
        return self.callbacks.get(callback_name)


# Example usage:
if __name__ == "__main__":
    callbacks_manager = ButtonCallbacks()

    # Get and call a callback
    insert_0_callback = callbacks_manager.get_callback("insert_0")
    if insert_0_callback:
        insert_0_callback()

    # Get and call a callback with arguments
    select_number_system = callbacks_manager.get_callback(
        "select_number_system"
    )
    if select_number_system:
        select_number_system("numsys", "hex")

    # Test all callbacks
    for callback_name, callback in callbacks_manager.callbacks.items():
        print(f"Testing {callback_name}:")
        if callback_name == "select_number_system":
            callback("numsys", "hex")
        elif callback_name == "select_bit_width":
            callback("bits", "bit_8")
        else:
            callback()

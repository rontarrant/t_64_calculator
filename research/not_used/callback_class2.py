from typing import Callable, Dict, Any

from callbacks import *
from button_data import *

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
		self.callback_functions: Dict[str, Callable[..., Any]] = {}
		self.initialize_callback_functions()
		self.initialize_callbacks()

	def initialize_callback_functions(self):
		"""
		Initializes the callback_functions dictionary.

		This method dynamically populates the callback_functions dictionary
		by iterating through the global namespace and adding functions
		defined in the 'callbacks' module.
		"""
		for name, obj in globals().items():
			if callable(obj) and obj.__module__ == "callbacks":
				self.callback_functions[name] = obj

	def initialize_callbacks(self):
		"""
		Initializes the callback functions.

		This method defines and stores the callback functions in the
		`callbacks` dictionary. Each key in the dictionary represents a
		specific button action, and the value is the corresponding
		callback function.
		"""
		for button_key, button_info in button_data.items():
			callback_name = button_info["callback"]
			callback_function = self.callback_functions.get(callback_name)

			if callback_function:
				self.callbacks[button_info["name"]] = callback_function
			else:
				print(f"Warning: Callback function '{callback_name}' not found in callback_functions for button '{button_info['name']}'.")

			# Handle button groups
			group_name = button_info["group"]
			if group_name != "none":
				if group_name not in self.button_groups:
					self.button_groups[group_name] = []
				self.button_groups[group_name].append(button_info["name"])


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
	'''
	# Get and call a callback
	insert_0_callback = callbacks_manager.get_callback("digit_0")
	
	if insert_0_callback:
		insert_0_callback()
	
	# Get and call a callback with arguments
	select_number_system = callbacks_manager.get_callback("select_number_system")

	if select_number_system:
		select_number_system("numsys", "hex")
	'''
	# Test all callbacks
	print("Testing all callbacks...")
	for callback_name, callback in callbacks_manager.callbacks.items():
		print(f"Testing {callback_name}:")
		if callback_name == select_number_system:
			print("calling select_number_system")
			callback("numsys", "hex")
		elif callback_name == "select_bit_width":
			callback("bits", "bit_8")
		else:
			callback()

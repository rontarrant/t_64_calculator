from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QObject

def handle_numsys_change(main_window):
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")

		match button_label:
			case "BIN":
				numsys = "bin"
				main_window._set_digit_button_states(binary_mode=True)
			case "DEC":
				numsys = "dec"
				main_window._set_digit_button_states(decimal_mode=True)
			case "HEX":
				numsys = "hex"
				main_window._set_digit_button_states(hexadecimal_mode=True)

	# Check each button and match its label to the button that was clicked
	# and make that the active button.
	for button_id, button in main_window.numsys_buttons.items():
		is_active = button.properties.get("label").lower() == numsys
		button.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["numsys"] = button
			print(f"\tNumber system button clicked: {button_label}, ID: {button_id}")
		button.update()

def handle_bitwidth_change(main_window):
	clicked_button = main_window.sender()

	if clicked_button:
		button_label = clicked_button.properties.get('label')
		print("button_label: ", button_label)
	
	for button_id, button in main_window.bitwidth_buttons.items():
		is_active = button.properties.get("label").lower() == button_label
		button.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["bits"] = button
			print(f"\tBit width button clicked: {button_label} ID: {button_id}")

		button.update()

def insert_digit(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tInserting 0... main_window: ", main_window, ", button: ", button_label)

def set_math_operation(main_window):
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")
		print("math operation: ", button_label)

def edit_operation(main_window):
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")
		print("edit operation: ", button_label)

def do_equals(main_window): # equals button
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tInserting 0... main_window: ", main_window, ", button: ", button_label)
	print("\tDoing equals...")

def about(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tInserting 0... main_window: ", main_window, ", button: ", button_label)
	print("\tShowing about dialog...")

def toggle_signed(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print(f"\tChanging the signed/unsigned state... {button_label}")

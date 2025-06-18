from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QObject

# state flags
signed_state = False
numsys_state = "dec"
bitwidth_state = "8"
operation_flag = None
one_number_op = False

def print_state_flags():
	print("signed_state: ", signed_state)
	print("numsys_state: ", numsys_state)
	print("bitwidth_state: ", bitwidth_state)
	print("operation_flag:", operation_flag)
	print("one_number_op:", one_number_op)

	print("")

print_state_flags()


def handle_numsys_change(main_window):
	global numsys_state
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

	numsys_state = numsys
	print_state_flags()


def handle_bitwidth_change(main_window):
	global bitwidth_state
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
	
	bitwidth_state = button_label
	print_state_flags()


def insert_digit(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tInserting 0... main_window: ", main_window, ", button: ", button_label)


def do_one_number_operation(flag):
	print("Doing one number operation: ", flag)


def set_math_operation(main_window):
	global operation_flag
	global one_number_op
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")
		print("math operation: ", button_label)
	
	operation_flag = button_label

	match operation_flag:
		case "NOT":
			one_number_op = True
		case "<<":
			one_number_op = True
		case ">>":
			one_number_op = True
		case _:
			one_number_op = False

	print_state_flags()

	if one_number_op == True:
		do_one_number_operation(operation_flag)


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
	global signed_state
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")

	if signed_state == False:
		signed_state = True
	else:
		signed_state = False

	main_window.sender().set_active(signed_state)

	print_state_flags()
	print(f"\tChanging the signed/unsigned state... {button_label}")

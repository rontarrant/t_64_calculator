import sys

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QObject

from math_functions_signed_bits import *
from math_functions_bits import *

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

#print_state_flags()

# input labels for digits, math/logic symbols, and results
first_input_label = None
second_input_label = None
operation_symbol_label = None
results_output_label = None
current_label = None

def register_labels(first_input, second_input, operation_label, results_output):
	global first_input_label
	global second_input_label
	global operation_symbol_label
	global results_output_label
	global current_label

	first_input_label = first_input
	second_input_label = second_input
	operation_symbol_label = operation_label
	results_output_label = results_output
	current_label = first_input_label


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
	#print_state_flags()


def handle_bitwidth_change(main_window):
	global bitwidth_stateresults_label
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
	#print_state_flags()


def insert_digit(main_window):
	global current_label
	global results_output_label

	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")

	# BEFORE adding the digit, check to see if results_label
	# has a value. If so, clear everything.
	if results_output_label.text() != "":
		first_input_label.setText("")
		second_input_label.setText("")
		results_output_label.setText("")
		operation_symbol_label.setText("")

	# add the current digit to the end of the current label
	content = current_label.text()
	content += button_label
	current_label.setText(content)

	#print("\tInserting... main_window: ", main_window, ", button: ", button_label)


def do_one_number_operation(op_type):
	#print("Doing one number operation: ", op_type)
	global first_input_label
	global results_output_label

	number = int(first_input_label.text())

	try:
		if op_type == "NOT":
				result = (~number) & ((1 << int(bitwidth_state)) - 1)
				#print("matched: ", op_type, ", result: ", result)
		elif op_type == "shl":
				result = (number << 1) & ((1 << int(bitwidth_state)) - 1)
		elif op_type == "shr":
				if signed_state:
					result = number >> 1
				else:
					result = (number % (1 << int(bitwidth_state))) >> 1
		else:
				print(f"Unknown one-operand operation: {op_type}", file = sys.stderr)
				return

		results_output_label.setText(str(result))

	except Exception as e:
		print(f"Error during one-operand operation {op_type}: {e}", file = sys.stderr)
		current_label = 0


def do_two_number_operation(op_type):
	global current_label
	global first_input_label
	global second_input_label

	#print("Doing two-number operation: ", op_type)

	# show the math/logic symbol in the UI
	operation_symbol_label.setText(op_type)
	# focus goes from first_input_label to second_input_label
	current_label = second_input_label


def set_math_operation(main_window):
	global operation_flag
	global one_number_op
	clicked_button = main_window.sender()

	if first_input_label.text() != "":
		if clicked_button:
			button_label = clicked_button.properties.get("label")
			#print("math operation: ", button_label)
		
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

		#print_state_flags()

		if one_number_op == True:
			do_one_number_operation(operation_flag)
		else:
			do_two_number_operation(operation_flag)


def edit_operation(main_window):
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")

		if button_label == "BS":
			content = current_label.text()
			content = content[:-1]
			current_label.setText(content)
		elif button_label == "CLR":
			current_label.setText("")
			
		#print("edit operation: ", button_label)


def do_equals(main_window): # equals button
	global signed_state
	global numsys_state
	global bitwidth_state
	global operation_flag
	global current_label
	global first_input_label
	global results_output_label

	clicked_button = main_window.sender()
	#button_label = clicked_button.properties.get("label")
	#print("\tmain_window: ", main_window, ", button: ", button_label)

	if operation_flag != None:
		#print("\tDoing equals... flags are:")
		#print_state_flags()
		bitwidth = int(bitwidth_state)
		first_number = int(first_input_label.text())
		second_number = int(second_input_label.text())

		match operation_flag:
			case "+":
				result = add_bits(first_number, second_number, bitwidth)
			case "-":
				result = subtract_bits(first_number, second_number, bitwidth)
			case "*":
				result = multiply_bits(first_number, second_number, bitwidth)
			case "/":
				result = divide_bits(first_number, second_number, bitwidth)
	else:
		pass
		#print("no operation current")
	
	results_output_label.setText(str(result[0]))
	# find the appropriate math/logic function

	# And reset the flag, indicating the operation is finished
	operation_flag = None
	#print("first_input: ", main_window.first_input)
	current_label = first_input_label

def about(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tmain_window: ", main_window, ", button: ", button_label)
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

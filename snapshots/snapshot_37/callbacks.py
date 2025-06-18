import sys
from icecream import ic

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QObject

from math_functions_signed_bits import *
from math_functions_bits import *
from base_converters import *
from bit_wise_operations_signed import *
from bit_wise_operations_unsigned import *

sign_set_values = {True: "Negative", False: "Positive"}
signed_unsigned_flags = {True: "Signed", False: "Unsigned"}

# state flags
signed_mode = False
sign_set_state = False
numsys_state = "dec"
bitwidth_state = "8"
operation_flag = None
one_number_op = False

def print_state_flags():
	print("State Flags:")
	print("signed_mode: ", signed_mode)
	print("signed_mode: ", signed_unsigned_flags[signed_mode])

	print("sign_set_state: ", sign_set_state)
	print("sign_set_state: ", sign_set_values[sign_set_state])

	print("numsys_state: ", numsys_state)
	print("bitwidth_state: ", bitwidth_state)
	print("operation_flag:", operation_flag)
	print("one_number_op:", one_number_op)

	print("")

# input labels for digits, math/logic symbols, and results
first_input_label = None
second_input_label = None
operation_symbol_label = None
results_output_label = None
current_label = None

def register_labels(first_input, second_input, operation_label,
						  results_output, remainder_output):
	global first_input_label
	global second_input_label
	global operation_symbol_label
	global results_output_label
	global current_label
	global remainder_label

	first_input_label = first_input
	second_input_label = second_input
	operation_symbol_label = operation_label
	results_output_label = results_output
	current_label = first_input_label
	remainder_label = remainder_output


def handle_numsys_change(main_window):
	global numsys_state
	global first_input_label
	global second_input_label
	global results_output_label
	global remainder_label
	clicked_button = main_window.sender()

	old_numsys = numsys_state

	ic("handle_numsys_change() start")
	print_state_flags()

	# get the new number system
	if clicked_button:
		button_label = clicked_button.properties.get("label")

		match button_label:
			case "BIN":
				numsys = "bin"
				main_window._set_digit_button_states(binary_mode = True)
			case "DEC":
				numsys = "dec"
				main_window._set_digit_button_states(decimal_mode = True)
			case "HEX":
				numsys = "hex"
				main_window._set_digit_button_states(hexadecimal_mode = True)

	# Check each button and match its label to the button that was clicked
	# and make that the active button.
	for button_id, button in main_window.numsys_buttons.items():
		is_active = button.properties.get("label").lower() == numsys
		button.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["numsys"] = button

		button.update()

	numsys_state = numsys

	if first_input_label != "":
		first_input_label.setText(select_conversion(old_numsys, numsys, first_input_label.text()))
	
	if second_input_label != "":
		second_input_label.setText(select_conversion(old_numsys, numsys, second_input_label.text()))

	if results_output_label != "":
		results_output_label.setText(select_conversion(old_numsys, numsys, results_output_label.text()))

	#ic("handle_numsys_change() end")
	#print_state_flags()


def handle_bitwidth_change(main_window):
	global bitwidth_state
	clicked_button = main_window.sender()

	ic("handle_bitwidth_change() start")
	print_state_flags()

	if clicked_button:
		button_label = clicked_button.properties.get('label')
	
	for button_id, button in main_window.bitwidth_buttons.items():
		is_active = button.properties.get("label").lower() == button_label
		button.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["bits"] = button

		button.update()
	
	bitwidth_state = button_label

	ic("handle_bitwidth_change() end")
	print_state_flags()


def insert_digit(main_window):
	global current_label
	global results_output_label
	global remainder_label

	clicked_button = main_window.sender()
	digit_to_add = clicked_button.properties.get("label")

	# BEFORE adding the digit, check to see if results_label
	# has a value. If so, clear everything.
	if results_output_label.text() != "":
		#print("starting a new calculation.")
		first_input_label.setText("")
		second_input_label.setText("")
		results_output_label.setText("")
		operation_symbol_label.setText("")
		remainder_label.setText("")


	# add the current digit to the end of the current label
	content = current_label.text()
	#ic("content: ", content, ", digit to add: ", digit_to_add)
	content += digit_to_add
	current_label.setText(content)


def do_one_number_operation(op_type):
	global first_input_label
	global results_output_label

	#ic("do_one_number_operation() start")
	#print_state_flags()

	number = int(first_input_label.text())

	try:
		if op_type == "NOT":
				result = (~number) & ((1 << int(bitwidth_state)) - 1)
		else:
				return

		results_output_label.setText(str(result))

	except Exception as e:
		print(f"Error during one-operand operation {op_type}: {e}", file = sys.stderr)
		current_label = 0

	#ic("do_one_number_operation() end")
	#print_state_flags()


def do_two_number_operation(op_type):
	global current_label
	global first_input_label
	global second_input_label

	# show the math/logic symbol in the UI
	operation_symbol_label.setText(op_type)
	# focus goes from first_input_label to second_input_label
	current_label = second_input_label


def set_math_operation(main_window):
	global operation_flag
	global one_number_op
	global signed_mode
	global sign_set_state
	sign_set_button = main_window.sign_set_button

	#ic("set_math_operation() start")
	#print_state_flags()

	clicked_button = main_window.sender()

	if first_input_label.text() != "":
		if clicked_button:
			button_label = clicked_button.properties.get("label")
		
		operation_flag = button_label

		match operation_flag:
			case "NOT":
				one_number_op = True
			case _:
				one_number_op = False

		'''
			case "<<":
				one_number_op = True
			case ">>":
				one_number_op = True
		'''

		if one_number_op == True:
			do_one_number_operation(operation_flag)
		else:
			do_two_number_operation(operation_flag)

		#signed_mode = False

		if sign_set_button._text == sign_set_button.properties["alt_label"]:
			sign_set_state = False
			sign_set_button._text = sign_set_button.properties["label"]
			sign_set_button.update()

	#ic("set_math_operation() end")
	#print_state_flags()


def edit_operation(main_window):
	clicked_button = main_window.sender()

	ic("edit_operation start")
	print_state_flags()

	if clicked_button:
		button_label = clicked_button.properties.get("label")

		if button_label == "BS":
			content = current_label.text()
			content = content[:-1]
			current_label.setText(content)
		elif button_label == "CLR":
			current_label.setText("")
	
	ic("edit_operation end")
	print_state_flags()


def select_math_function(operation_flag):
	math_function = None

	if operation_flag != None:
		if signed_mode == False:
			match operation_flag:
				case "+":
					math_function = add_bits
				case "-":
					math_function = subtract_bits
				case "*":
					math_function = multiply_bits
				case "/":
					math_function = divide_bits
				case "AND":
					math_function = bitwise_and
				case "XOR":
					math_function = bitwise_xor
				case "OR":
					math_function = bitwise_or
				case "<<":
					math_function = shift_left
				case ">>":
					math_function = shift_right
		elif signed_mode == True:
			match operation_flag:
				case "+":
					math_function = add_signed_bits
				case "-":
					math_function = subtract_signed_bits
				case "*":
					math_function = multiply_signed_bits
				case "/":
					math_function = divide_signed_bits
				case "AND":
					math_function = bitwise_and_signed
				case "XOR":
					math_function = bitwise_xor_signed
				case "OR":
					math_function = bitwise_or_signed
				case "<<":
					math_function = shift_left_signed
				case ">>":
					math_function = shift_right_signed

	return math_function


def do_equals(main_window): # equals button
	global signed_mode
	global numsys_state
	global bitwidth_state
	global operation_flag
	global current_label
	global first_input_label
	global results_output_label
	global remainder_label

	#ic("do_equals start")
	#print_state_flags()

	if operation_flag != None:
		bitwidth = int(bitwidth_state)
		first_number = first_input_label.text()
		second_number = second_input_label.text()

		# if the base is non-decimal, convert
		if numsys_state == "hex":
			first_number = hexadecimal_to_decimal(first_number)
			second_number = hexadecimal_to_decimal(second_number)
		elif numsys_state == "bin":
			first_number = binary_to_decimal(first_number)
			second_number = binary_to_decimal(second_number)
		else:
			first_number = int(first_input_label.text())
			second_number = int(second_input_label.text())

		# Get math/logic function for the current operation...
		two_number_math = select_math_function(operation_flag)
		# and call it.
		result = two_number_math(first_number, second_number, bitwidth)

		# if the base is non-decimal, convert back to current base
		if numsys_state == "hex":
			display_result = decimal_to_hexadecimal(int(result[0])).upper()
		elif numsys_state == "bin":
			display_result = decimal_to_binary(int(result[0]))

			if operation_flag == "/":
				remainder_result = decimal_to_binary(int(result[1]))

				# divide by zero? Display "NaN" in results_output_label
				if result[2] == True:
					display_result = "NaN"
		else:
			display_result = result[0]

		# show the result
		results_output_label.setText(str(display_result))

		# Is there a remainder? Display it.
		if operation_flag == "/":
			remainder_label.setText("R: " + str(remainder_result))
	else:
		pass

	# And reset the flag, indicating the operation is finished
	operation_flag = None
	current_label = first_input_label

	#ic("do_equals end")
	#print_state_flags()

def about(main_window):
	clicked_button = main_window.sender()
	button_label = clicked_button.properties.get("label")
	print("\tmain_window: ", main_window, ", button: ", button_label)
	print("\tShowing about dialog...")


def set_sign(main_window):
	global sign_set_state
	global current_label
	global signed_mode

	# get the sign-switch button
	clicked_button = main_window.sign_set_button

	#ic("set_sign() start")
	#ic(sign_set_state, signed_mode, current_label.text(), clicked_button._text)
	#print_state_flags()


	# signed_mode is set (below) by the toggle-sign button
	if signed_mode == True:
		# what's showing on the label?
		if "-" in current_label.text():
			# remove the minus sign from the current number
			number = current_label.text()[1:]
			# change the button text
			clicked_button._text = clicked_button.properties["label"]
			clicked_button.update()
			sign_set_state = False
		else:
			# prepend a minus sign
			ic("prepend -")
			number = "-" + current_label.text()
			# change the button text
			clicked_button._text = clicked_button.properties["alt_label"]
			clicked_button.update()
			sign_set_state = True

		# update the current number
		current_label.setText(number)

	# change the active state of the switch-sign button
	clicked_button.set_active(signed_mode)

	#ic("set_sign() end")
	#ic(sign_set_state, signed_mode, current_label.text(), clicked_button._text)
	#print_state_flags()


def sign_mode_toggle(main_window):
	global signed_mode
	global current_label
	clicked_button = main_window.sender()
	sign_set_button = main_window.sign_set_button

	#ic("sign_mode_toggle() start")
	#print_state_flags()

	# if we're in unsigned mode, go to signed mode
	if signed_mode == False:
		signed_mode = True
	# if we're in signed mode, go to unsigned mode
	else:
		signed_mode = False
		# if the switch-sign button is "-", change the label
		if sign_set_button._text == sign_set_button.properties["alt_label"]:
			# change the button text to "+"
			sign_set_button._text = sign_set_button.properties["label"]
			# if there's minus sign in the current number
			if current_label.text()[:1] == "-":
				# remove the minus sign
				number = current_label.text()[1:]
				# update the current number
				current_label.setText(number)
			else:
				# leave the number as is
				number = current_label.text()


	main_window.sender().set_active(signed_mode)
	sign_set_button.set_active(signed_mode)
	sign_set_button.setEnabled(signed_mode)
	sign_set_button.update()

	#ic("sign_mode_toggle() end")
	#print_state_flags()

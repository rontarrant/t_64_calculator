def set_binary_number_system(main_window):
	print("\tSwitching to: binary...")
	if "bin" in main_window.buttons:
		main_window.buttons["bin"].set_active(True)
		main_window.active_radio_buttons["numsys"] = main_window.buttons["bin"]
	if "dec" in main_window.buttons:
		main_window.buttons["dec"].set_active(False)
	if "hex" in main_window.buttons:
		main_window.buttons["hex"].set_active(False)

	if "dot" in main_window.buttons:
		main_window.buttons["dot"].setEnabled(False)
		main_window.buttons["dot"].set_active(False)
		main_window.buttons["dot"].update()

	_update_numsys_button_states(main_window)
	_update_hex_digit_button_states(main_window)

def set_decimal_number_system(main_window):
	print("\tSwitching to: decimal...")
	if "bin" in main_window.buttons:
		main_window.buttons["bin"].set_active(False)
	if "dec" in main_window.buttons:
		main_window.buttons["dec"].set_active(True)
		main_window.active_radio_buttons["numsys"] = main_window.buttons["dec"]
	if "hex" in main_window.buttons:
		main_window.buttons["hex"].set_active(False)

	if "dot" in main_window.buttons:
		main_window.buttons["dot"].setEnabled(True)
		main_window.buttons["dot"].set_active(True)
		main_window.buttons["dot"].update()

	_update_numsys_button_states(main_window)
	_update_hex_digit_button_states(main_window)

def set_hexadecimal_number_system(main_window):
	print("\tSwitching to: hexadecimal...")
	if "bin" in main_window.buttons:
		main_window.buttons["bin"].set_active(False)
	if "dec" in main_window.buttons:
		main_window.buttons["dec"].set_active(False)
	if "hex" in main_window.buttons:
		main_window.buttons["hex"].set_active(True)
		main_window.active_radio_buttons["numsys"] = main_window.buttons["hex"]

	if "dot" in main_window.buttons:
		main_window.buttons["dot"].setEnabled(False)
		main_window.buttons["dot"].set_active(False)
		main_window.buttons["dot"].update()

	_update_numsys_button_states(main_window)
	_update_hex_digit_button_states(main_window)

def _update_numsys_button_states(main_window):
	if "bin" in main_window.buttons:
		main_window.buttons["bin"].update()
	if "dec" in main_window.buttons:
		main_window.buttons["dec"].update()
	if "hex" in main_window.buttons:
		main_window.buttons["hex"].update()

def _update_hex_digit_button_states(main_window):
	hex_digit_ids = ["a", "b", "c", "d", "e", "f"]
	decimal_digit_ids = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	active_numsys = main_window.active_radio_buttons["numsys"]

	# Handle hexadecimal digits
	enable_hex = False
	if active_numsys and active_numsys.properties.get("label") == "HEX":
		enable_hex = True
	for button_id in hex_digit_ids:
		if button_id in main_window.buttons:
			main_window.buttons[button_id].setEnabled(enable_hex)
			main_window.buttons[button_id].set_active(enable_hex) # Keep visual state consistent
			main_window.buttons[button_id].update()

	# Handle decimal digits
	if active_numsys and active_numsys.properties.get("label") == "BIN":
		for button_id in decimal_digit_ids:
			if button_id in main_window.buttons:
				is_enabled = (button_id == "0" or button_id == "1")
				main_window.buttons[button_id].setEnabled(is_enabled)
				main_window.buttons[button_id].set_active(is_enabled) # Keep visual state consistent
				main_window.buttons[button_id].update()
	elif active_numsys and (active_numsys.properties.get("label") == "DEC" or active_numsys.properties.get("label") == "HEX"):
		for button_id in decimal_digit_ids:
			if button_id in main_window.buttons:
				main_window.buttons[button_id].setEnabled(True)
				main_window.buttons[button_id].set_active(True) # Keep visual state consistent
				main_window.buttons[button_id].update()
	elif not active_numsys:
		# Enable all digits if no number system is selected
		for button_id in decimal_digit_ids + hex_digit_ids:
			if button_id in main_window.buttons:
				main_window.buttons[button_id].setEnabled(True)
				main_window.buttons[button_id].set_active(True) # Keep visual state consistent
				main_window.buttons[button_id].update()

def set_8_bit_width(main_window):
	print("\tSwitching to: 8-bit...")
	if "bit_8" in main_window.buttons:
		main_window.buttons["bit_8"].set_active(True)
	if "bit_16" in main_window.buttons:
		main_window.buttons["bit_16"].set_active(False)
	if "bit_32" in main_window.buttons:
		main_window.buttons["bit_32"].set_active(False)
	_update_bitwidth_button_states(main_window)

def set_16_bit_width(main_window):
	print("\tSwitching to: 16-bit...")
	if "bit_8" in main_window.buttons:
		main_window.buttons["bit_8"].set_active(False)
	if "bit_16" in main_window.buttons:
		main_window.buttons["bit_16"].set_active(True)
	if "bit_32" in main_window.buttons:
		main_window.buttons["bit_32"].set_active(False)
	_update_bitwidth_button_states(main_window)

def set_32_bit_width(main_window):
	print("\tSwitching to: 32-bit...")
	if "bit_8" in main_window.buttons:
		main_window.buttons["bit_8"].set_active(False)
	if "bit_16" in main_window.buttons:
		main_window.buttons["bit_16"].set_active(False)
	if "bit_32" in main_window.buttons:
		main_window.buttons["bit_32"].set_active(True)
	_update_bitwidth_button_states(main_window)

def _update_bitwidth_button_states(main_window):
	if "bit_8" in main_window.buttons:
		main_window.buttons["bit_8"].update()
	if "bit_16" in main_window.buttons:
		main_window.buttons["bit_16"].update()
	if "bit_32" in main_window.buttons:
		main_window.buttons["bit_32"].update()

def insert_0(main_window):
	print("\tInserting 0...")

def insert_1(main_window):
	print("\tInserting 1...")

def insert_2(main_window):
	print("\tInserting 2...")

def insert_3(main_window):
	print("\tInserting 3...")

def insert_4(main_window):
	print("\tInserting 4...")

def insert_5(main_window):
	print("\tInserting 5...")

def insert_6(main_window):
	print("\tInserting 6...")

def insert_7(main_window):
	print("\tInserting 7...")

def insert_8(main_window):
	print("\tInserting 8...")

def insert_9(main_window):
	print("\tInserting 9...")

def insert_a(main_window):
	print("\tInserting A...")

def insert_b(main_window):
	print("\tInserting B...")

def insert_c(main_window):
	print("\tInserting C...")

def insert_d(main_window):
	print("\tInserting D...")

def insert_e(main_window):
	print("\tInserting E...")

def insert_f(main_window):
	print("\tInserting F...")

def about(main_window):
	print("\tShowing about dialog...")

def toggle_signed(main_window):
	print("\tChanging the signed/unsigned state...")

def insert_division(main_window):
	print("\tInserting a divide sign...")

def insert_multiply(main_window):
	print("\tInserting a multiply sign...")

def insert_subtract(main_window):
	print("\tInserting a subtract sign...")

def insert_addition(main_window):
	print("\tInserting an addition sign...")

def insert_dot(main_window):
	print("\tInserting a dot...")

def insert_left_bracket(main_window):
	print("\tInserting a left bracket...")

def insert_right_bracket(main_window):
	print("\tInserting a right bracket..")

def clear_display(main_window):
	print("\tClearing the input")

def do_backspace(main_window):
	print("\tBackspacing...")

def do_and(main_window):
	print("\tperforming AND...")

def do_or(main_window):
	print("\tperforming OR...")
	
def do_xor(main_window):
	print("\tperforming XOR...")
	
def do_not(main_window):
	print("\tperforming NOT...")
	
def do_equals(main_window): # equals button
	print("\tDoing equals...")

def do_shift_left(main_window):
	print("\tDoing shift left <<")

def do_shift_right(main_window):
	print("\tDoing shift right >>")

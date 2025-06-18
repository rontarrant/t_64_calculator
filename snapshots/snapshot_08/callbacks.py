from PySide6.QtCore import QObject

def handle_numsys_change(main_window):
	clicked_button = main_window.sender()
	
	if clicked_button:
		button_label = clicked_button.properties.get("label")
		print(f"\tNumber system button clicked: {button_label}")

		if button_label == "BIN":
			_set_number_system(main_window, "bin")
		elif button_label == "DEC":
			_set_number_system(main_window, "dec")
		elif button_label == "HEX":
			_set_number_system(main_window, "hex")
	else:
		print("\tError: sender() did not return a QPushButton object in handle_numsys_change.")

def _set_number_system(main_window, numsys):
	for btn_id, btn in main_window.numsys_buttons.items(): # Iterate through numsys_buttons
		is_active = btn.properties.get("label").lower() == numsys
		btn.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["numsys"] = btn
		btn.update()

	if numsys == "bin":
		main_window._set_digit_button_states(binary_mode=True)
	elif numsys == "dec":
		main_window._set_digit_button_states(decimal_mode=True)
	elif numsys == "hex":
		main_window._set_digit_button_states(hexadecimal_mode=True)

def handle_bitwidth_change(main_window):
	clicked_button = main_window.sender()

	if clicked_button:
		combined_label = f"{clicked_button.properties.get('label')}-{clicked_button.properties.get('sublabel')}"
		print(f"\tBit width button clicked: {combined_label}")

		if combined_label == "8-BIT":
			_set_bitwidth(main_window, "8")
		elif combined_label == "16-BIT":
			_set_bitwidth(main_window, "16")
		elif combined_label == "32-BIT":
			_set_bitwidth(main_window, "32")
	else:
		print("\tError: sender() did not return a QPushButton object in handle_bitwidth_change.")

def _set_bitwidth(main_window, bits):
	for btn_id, btn in main_window.bitwidth_buttons.items():
		# We still use the 'label' for setting the active state in _set_bitwidth
		is_active = btn.properties.get("label") == bits
		btn.set_active(is_active)

		if is_active:
			main_window.active_radio_buttons["bits"] = btn
		btn.update()

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

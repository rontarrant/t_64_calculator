def rol(n, shifts, bit_width = 8):
	"""
	Performs a Rotate Left (ROL) operation on a number.

	Args:
		n (int): The number to rotate.
		shifts (int): The number of positions to rotate left.
		bit_width (int): The number of bits in the integer (e.g., 8 for byte, 16 for word).

	Returns:
		int: The rotated number.
	"""
	# Ensure shifts are within the bit_width to avoid unnecessary large shifts
	shifts %= bit_width

	# Get the bits that would "fall off" the left end
	# These bits are then shifted to the right end
	# (n << shifts) & ((1 << bit_width) - 1) handles the main left shift and masks to the bit_width
	# (n >> (bit_width - shifts)) handles the bits that wrap around
	return ((n << shifts) | (n >> (bit_width - shifts))) & ((1 << bit_width) - 1)

def ror(n, shifts, bit_width = 8):
	"""
	Performs a Rotate Right (ROR) operation on a number.

	Args:
		n (int): The number to rotate.
		shifts (int): The number of positions to rotate right.
		bit_width (int): The number of bits in the integer (e.g., 8 for byte, 16 for word).

	Returns:
		int: The rotated number.
	"""
	# Ensure shifts are within the bit_width
	shifts %= bit_width

	# Get the bits that would "fall off" the right end
	# These bits are then shifted to the left end
	# (n >> shifts) handles the main right shift
	# (n << (bit_width - shifts)) & ((1 << bit_width) - 1) handles the bits that wrap around and masks
	return ((n >> shifts) | (n << (bit_width - shifts))) & ((1 << bit_width) - 1)

# --- Examples ---

if __name__ == "__main__":
	# 8-bit examples (like C-64 byte operations)
	print("--- 8-bit Examples ---")
	num_8bit = 0b00001010  # Decimal 10
	print(f"Original 8-bit: {bin(num_8bit)} (Decimal: {num_8bit})")

	# ROL 1
	rotated_left_8bit = rol(num_8bit, 1, 8)
	print(f"ROL 1 (8-bit):    {bin(rotated_left_8bit)} (Decimal: {rotated_left_8bit})") # Expected: 0b00010100 (Decimal 20)

	# ROR 1
	rotated_right_8bit = ror(num_8bit, 1, 8)
	print(f"ROR 1 (8-bit):    {bin(rotated_right_8bit)} (Decimal: {rotated_right_8bit})") # Expected: 0b01000101 (Decimal 69)

	# ROL with MSB wrap
	num_8bit_msb = 0b10000000 # Decimal 128
	print(f"\nOriginal 8-bit: {bin(num_8bit_msb)} (Decimal: {num_8bit_msb})")
	rotated_left_msb = rol(num_8bit_msb, 1, 8)
	print(f"ROL 1 (8-bit):    {bin(rotated_left_msb)} (Decimal: {rotated_left_msb})") # Expected: 0b00000001 (Decimal 1)

	# ROR with LSB wrap
	num_8bit_lsb = 0b00000001 # Decimal 1
	print(f"\nOriginal 8-bit: {bin(num_8bit_lsb)} (Decimal: {num_8bit_lsb})")
	rotated_right_lsb = ror(num_8bit_lsb, 1, 8)
	print(f"ROR 1 (8-bit):    {bin(rotated_right_lsb)} (Decimal: {rotated_right_lsb})") # Expected: 0b10000000 (Decimal 128)

	# 16-bit example
	print("\n--- 16-bit Example ---")
	num_16bit = 0b1000000000000001 # Decimal 32769
	print(f"Original 16-bit: {bin(num_16bit)} (Decimal: {num_16bit})")

	rotated_left_16bit = rol(num_16bit, 4, 16)
	print(f"ROL 4 (16-bit):   {bin(rotated_left_16bit)} (Decimal: {rotated_left_16bit})")

	rotated_right_16bit = ror(num_16bit, 4, 16)
	print(f"ROR 4 (16-bit):   {bin(rotated_right_16bit)} (Decimal: {rotated_right_16bit})")

	# Example for shifts greater than bit_width
	num_test = 0b00001111
	print(f"\nOriginal test: {bin(num_test)}")
	rotated_test = rol(num_test, 9, 8) # Equivalent to ROL 1
	print(f"ROL 9 (8-bit):    {bin(rotated_test)} (Decimal: {rotated_test})") # Expected: 0b00011110 (Decimal 30)

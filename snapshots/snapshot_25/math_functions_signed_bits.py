def add_signed_bits(a, b, bits):
	"""Adds two signed integers with specified bit width and handles overflow."""
	if bits == 8:
		mask = 0xFF
		min_val, max_val = -128, 127
	elif bits == 16:
		mask = 0xFFFF
		min_val, max_val = -32768, 32767
	elif bits == 32:
		mask = 0xFFFFFFFF
		min_val, max_val = -2147483648, 2147483647
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	# Convert inputs to signed integers
	a = (a & mask) - (mask + 1 if a & (mask + 1) // 2 else 0)
	b = (b & mask) - (mask + 1 if b & (mask + 1) // 2 else 0)

	result = a + b

	if result < min_val or result > max_val:
		result = ((result + (max_val + 1)) % (2 * (max_val + 1))) - (max_val + 1)
		overflow = True
	else:
		overflow = False

	return result, overflow


def subtract_signed_bits(a, b, bits):
	"""Subtracts two signed integers with specified bit width and handles underflow."""
	if bits == 8:
		mask = 0xFF
		min_val, max_val = -128, 127
	elif bits == 16:
		mask = 0xFFFF
		min_val, max_val = -32768, 32767
	elif bits == 32:
		mask = 0xFFFFFFFF
		min_val, max_val = -2147483648, 2147483647
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	# Convert inputs to signed integers
	a = (a & mask) - (mask + 1 if a & (mask + 1) // 2 else 0)
	b = (b & mask) - (mask + 1 if b & (mask + 1) // 2 else 0)

	result = a - b

	if result < min_val or result > max_val:
		result = ((result + (max_val + 1)) % (2 * (max_val + 1))) - (max_val + 1)
		underflow = True
	else:
		underflow = False

	return result, underflow


def multiply_signed_bits(a, b, bits):
	"""Multiplies two signed integers with specified bit width and handles overflow."""
	if bits == 8:
		mask = 0xFF
		min_val, max_val = -128, 127
	elif bits == 16:
		mask = 0xFFFF
		min_val, max_val = -32768, 32767
	elif bits == 32:
		mask = 0xFFFFFFFF
		min_val, max_val = -2147483648, 2147483647
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	# Convert inputs to signed integers
	a = (a & mask) - (mask + 1 if a & (mask + 1) // 2 else 0)
	b = (b & mask) - (mask + 1 if b & (mask + 1) // 2 else 0)

	result = a * b

	if result < min_val or result > max_val:
		result = ((result + (max_val + 1)) % (2 * (max_val + 1))) - (max_val + 1)
		overflow = True
	else:
		overflow = False

	return result, overflow


def divide_signed_bits(a, b, bits):
	"""Divides two signed integers with specified bit width and handles division by zero and underflow."""
	if bits == 8:
		mask = 0xFF
		min_val, max_val = -128, 127
	elif bits == 16:
		mask = 0xFFFF
		min_val, max_val = -32768, 32767
	elif bits == 32:
		mask = 0xFFFFFFFF
		min_val, max_val = -2147483648, 2147483647
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	# Convert inputs to signed integers
	a = (a & mask) - (mask + 1 if a & (mask + 1) // 2 else 0)
	b = (b & mask) - (mask + 1 if b & (mask + 1) // 2 else 0)

	if b == 0:
		return 0, 0, True  # Division by zero

	quotient = a // b
	remainder = a % b

	if quotient < min_val or quotient > max_val:
		quotient = ((quotient + (max_val + 1)) % (2 * (max_val + 1))) - (max_val + 1)
		underflow = True
	else:
		underflow = False

	return quotient, remainder, underflow


def test_add_signed_bits():
	print("--- Testing add_signed_bits ---")
	# 8-bit tests
	assert add_signed_bits(127, 1, 8) == (-128, True)  # Overflow
	assert add_signed_bits(-128, -1, 8) == (127, True)  # Underflow
	assert add_signed_bits(50, -20, 8) == (30, False)  # No overflow/underflow

	# 16-bit tests
	assert add_signed_bits(32767, 1, 16) == (-32768, True)  # Overflow
	assert add_signed_bits(-32768, -1, 16) == (32767, True)  # Underflow
	assert add_signed_bits(1000, -500, 16) == (500, False)  # No overflow/underflow

	# 32-bit tests
	assert add_signed_bits(2147483647, 1, 32) == (-2147483648, True)  # Overflow
	assert add_signed_bits(-2147483648, -1, 32) == (2147483647, True)  # Underflow
	assert add_signed_bits(1000000, -500000, 32) == (500000, False)  # No overflow/underflow

	print("add_signed_bits tests passed!")


def test_subtract_signed_bits():
	print("\n--- Testing subtract_signed_bits ---")
	# 8-bit tests
	assert subtract_signed_bits(-128, 1, 8) == (127, True)  # Underflow
	assert subtract_signed_bits(127, -1, 8) == (-128, True)  # Overflow
	assert subtract_signed_bits(50, 20, 8) == (30, False)  # No overflow/underflow

	# 16-bit tests
	assert subtract_signed_bits(-32768, 1, 16) == (32767, True)  # Underflow
	assert subtract_signed_bits(32767, -1, 16) == (-32768, True)  # Overflow
	assert subtract_signed_bits(1000, 500, 16) == (500, False)  # No overflow/underflow

	# 32-bit tests
	assert subtract_signed_bits(-2147483648, 1, 32) == (2147483647, True)  # Underflow
	assert subtract_signed_bits(2147483647, -1, 32) == (-2147483648, True)  # Overflow
	assert subtract_signed_bits(1000000, 500000, 32) == (500000, False)  # No overflow/underflow

	print("subtract_signed_bits tests passed!")


def test_multiply_signed_bits():
	print("\n--- Testing multiply_signed_bits ---")
	# 8-bit tests
	assert multiply_signed_bits(64, 2, 8) == (-128, True)  # Overflow
	assert multiply_signed_bits(-128, 2, 8) == (0, True)  # Underflow
	assert multiply_signed_bits(10, -3, 8) == (-30, False)  # No overflow/underflow

	# 16-bit tests
	assert multiply_signed_bits(16384, 2, 16) == (-32768, True)  # Overflow
	assert multiply_signed_bits(-32768, 2, 16) == (0, True)  # Underflow
	assert multiply_signed_bits(100, -20, 16) == (-2000, False)  # No overflow/underflow

	# 32-bit tests
	assert multiply_signed_bits(1073741824, 2, 32) == (-2147483648, True)  # Overflow
	assert multiply_signed_bits(-2147483648, 2, 32) == (0, True)  # Underflow
	assert multiply_signed_bits(10000, -300, 32) == (-3000000, False)  # No overflow/underflow

	print("multiply_signed_bits tests passed!")


def test_divide_signed_bits():
	print("\n--- Testing divide_signed_bits ---")
	# 8-bit tests
	assert divide_signed_bits(-128, 2, 8) == (-64, 0, False)  # No overflow/underflow
	assert divide_signed_bits(127, 2, 8) == (63, 1, False)  # No overflow/underflow
	assert divide_signed_bits(-128, 0, 8) == (0, 0, True)  # Division by zero

	# 16-bit tests
	assert divide_signed_bits(-32768, 2, 16) == (-16384, 0, False)  # No overflow/underflow
	assert divide_signed_bits(32767, 3, 16) == (10922, 1, False)  # No overflow/underflow
	assert divide_signed_bits(-32768, 0, 16) == (0, 0, True)  # Division by zero

	# 32-bit tests
	assert divide_signed_bits(-2147483648, 2, 32) == (-1073741824, 0, False)  # No overflow/underflow
	assert divide_signed_bits(2147483647, 3, 32) == (715827882, 1, False)  # No overflow/underflow
	assert divide_signed_bits(-2147483648, 0, 32) == (0, 0, True)  # Division by zero

	print("divide_signed_bits tests passed!")

if __name__ == "__main__":
	test_add_signed_bits()
	test_subtract_signed_bits()
	test_multiply_signed_bits()
	test_divide_signed_bits()

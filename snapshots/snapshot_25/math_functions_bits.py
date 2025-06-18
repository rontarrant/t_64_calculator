def add_bits(a, b, bits):
	"""Adds two integers with specified bit width and handles overflow."""
	if bits == 8:
		mask = 0xFF
		max_val = 255
	elif bits == 16:
		mask = 0xFFFF
		max_val = 65535
	elif bits == 32:
		mask = 0xFFFFFFFF
		max_val = 4294967295
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	a = a & mask
	b = b & mask

	result = a + b

	if result > max_val:
		result = result & mask
		overflow = True
	else:
		overflow = False

	return result, overflow

def subtract_bits(a, b, bits):
    """Subtracts two integers with specified bit width and handles underflow."""
    if bits == 8:
        mask = 0xFF
    elif bits == 16:
        mask = 0xFFFF
    elif bits == 32:
        mask = 0xFFFFFFFF
    else:
        raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

    a = a & mask
    b = b & mask

    result = a - b

    if result < 0:
        result = result & mask
        underflow = True
    else:
        underflow = False

    return result, underflow

def multiply_bits(a, b, bits):
	"""Multiplies two integers with specified bit width and handles overflow."""
	if bits == 8:
		mask = 0xFF
		max_val = 255
	elif bits == 16:
		mask = 0xFFFF
		max_val = 65535
	elif bits == 32:
		mask = 0xFFFFFFFF
		max_val = 4294967295
	else:
		raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

	a = a & mask
	b = b & mask

	result = a * b

	if result > max_val:
		result = result & mask
		overflow = True
	else:
		overflow = False

	return result, overflow


def divide_bits(a, b, bits):
    """
    Divides two integers with specified bit width, handling division by zero,
    and tests for potential underflow.
    """
    if bits == 8:
        mask = 0xFF
    elif bits == 16:
        mask = 0xFFFF
    elif bits == 32:
        mask = 0xFFFFFFFF
    else:
        raise ValueError("Invalid bit width. Must be 8, 16, or 32.")

    a = a & mask
    b = b & mask

    if b == 0:
        return 0, 0, True  # Division by zero

    quotient = a // b
    remainder = a % b

    # Test for underflow (quotient < minimum representable value for unsigned integers)
    if quotient < 0:  # This shouldn't happen for unsigned integers but added for robustness
        underflow = True
    else:
        underflow = False

    return quotient, remainder, underflow

def test_add_bits_complete():
	print("\n--- Comprehensive Testing add_bits ---")
	# 8-bit
	assert add_bits(255, 1, 8) == (0, True)  # Overflow
	assert add_bits(10, 5, 8) == (15, False)  # No overflow
	assert add_bits(250, 10, 8) == (4, True)  # Overflow

	# 16-bit
	assert add_bits(65535, 1, 16) == (0, True)  # Overflow
	assert add_bits(1000, 2000, 16) == (3000, False)  # No overflow
	assert add_bits(32768, 32768, 16) == (0, True)  # Overflow

	# 32-bit
	assert add_bits(4294967295, 1, 32) == (0, True)  # Overflow
	assert add_bits(1000000, 2000000, 32) == (3000000, False)  # No overflow
	assert add_bits(2147483648, 2147483648, 32) == (0, True)  # Overflow
	print("add_bits comprehensive tests passed!")


def test_subtract_bits_complete():
	print("\n--- Comprehensive Testing subtract_bits ---")
	# 8-bit
	assert subtract_bits(0, 1, 8) == (255, True)  # Underflow
	assert subtract_bits(20, 10, 8) == (10, False)  # No underflow
	assert subtract_bits(128, 129, 8) == (255, True)  # Underflow

	# 16-bit
	assert subtract_bits(0, 1, 16) == (65535, True)  # Underflow
	assert subtract_bits(1000, 500, 16) == (500, False)  # No underflow
	assert subtract_bits(32768, 65535, 16) == (32769, True)  # Underflow

	# 32-bit
	assert subtract_bits(0, 1, 32) == (4294967295, True)  # Underflow
	assert subtract_bits(3000000, 1000000, 32) == (2000000, False)  # No underflow
	assert subtract_bits(2147483648, 4294967295, 32) == (2147483649, True)  # Underflow
	print("subtract_bits comprehensive tests passed!")



def test_multiply_bits_complete():
	print("\n--- Comprehensive Testing multiply_bits ---")
	# 8-bit
	assert multiply_bits(16, 16, 8) == (0, True)  # Overflow
	assert multiply_bits(10, 5, 8) == (50, False)  # No overflow
	assert multiply_bits(25, 11, 8) == (19, True)  # Overflow

	# 16-bit
	assert multiply_bits(256, 256, 16) == (0, True)  # Overflow
	assert multiply_bits(200, 300, 16) == (60000, False)  # No overflow
	assert multiply_bits(32768, 2, 16) == (0, True)  # Overflow

	# 32-bit
	assert multiply_bits(65536, 65536, 32) == (0, True)  # Overflow
	assert multiply_bits(10000, 20000, 32) == (200000000, False)  # No overflow
	assert multiply_bits(2147483648, 2, 32) == (0, True)  # Overflow
	print("multiply_bits comprehensive tests passed!")


def test_divide_bits_complete():
	print("\n--- Comprehensive Testing divide_bits ---")
	# 8-bit
	assert divide_bits(255, 0, 8) == (0, 0, True)  # Division by zero
	assert divide_bits(200, 5, 8) == (40, 0, False)  # No underflow
	assert divide_bits(1, 2, 8) == (0, 1, False)  # No underflow, remainder present

	# 16-bit
	assert divide_bits(65535, 1, 16) == (65535, 0, False)  # No underflow
	assert divide_bits(32768, 3, 16) == (10922, 2, False)  # No underflow, remainder present
	assert divide_bits(1, 2, 16) == (0, 1, False)  # No underflow, result less than divisor

	# 32-bit
	assert divide_bits(4294967295, 1, 32) == (4294967295, 0, False)  # No underflow
	assert divide_bits(2147483648, 2, 32) == (1073741824, 0, False)  # No underflow
	assert divide_bits(1, 2, 32) == (0, 1, False)  # No underflow, remainder present
	print("divide_bits comprehensive tests passed!")


if __name__ == "__main__":
	test_add_bits_complete()
	test_subtract_bits_complete()
	test_multiply_bits_complete()
	test_divide_bits_complete()

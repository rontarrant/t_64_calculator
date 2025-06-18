def decimal_to_hexadecimal(decimal_num: int) -> str:
	"""Converts a decimal number to its hexadecimal representation."""
	if not isinstance(decimal_num, int):
		raise TypeError("Input must be an integer.")
   
	return hex(decimal_num)[2:]  # [2:] to remove the "0x" prefix

def decimal_to_binary(decimal_num: int) -> str:
	"""Converts a decimal number to its binary representation."""
	if not isinstance(decimal_num, int):
		raise TypeError("Input must be an integer.")
	
	return bin(decimal_num)[2:]  # [2:] to remove the "0b" prefix

def hexadecimal_to_decimal(hex_num_str: str) -> int:
	"""Converts a hexadecimal string to its decimal representation."""
	if not isinstance(hex_num_str, str):
		raise TypeError("Input must be a string.")
	
	return int(hex_num_str, 16)

def hexadecimal_to_binary(hex_num_str: str) -> str:
	"""Converts a hexadecimal string to its binary representation."""
	if not isinstance(hex_num_str, str):
		raise TypeError("Input must be a string.")
	decimal_num = int(hex_num_str, 16)

	return bin(decimal_num)[2:]

def binary_to_hexadecimal(binary_num_str: str) -> str:
	"""Converts a binary string to its hexadecimal representation."""
	if not isinstance(binary_num_str, str):
		raise TypeError("Input must be a string.")
	decimal_num = int(binary_num_str, 2)

	return hex(decimal_num)[2:]

def binary_to_decimal(binary_num_str: str) -> int:
	"""Converts a binary string to its decimal representation."""
	if not isinstance(binary_num_str, str):
		raise TypeError("Input must be a string.")
	
	return int(binary_num_str, 2)

if __name__ == "__main__":
	# 8-bit examples
	decimal_8_bit = 254  # Max 8-bit unsigned
	hex_8_bit_str = "FF"
	binary_8_bit_str = "11111111"

	print(f"Decimal {decimal_8_bit} to Hex: {decimal_to_hexadecimal(decimal_8_bit)}")
	print(f"Decimal {decimal_8_bit} to Binary: {decimal_to_binary(decimal_8_bit)}")
	print(f"Hex '{hex_8_bit_str}' to Decimal: {hexadecimal_to_decimal(hex_8_bit_str)}")
	print(f"Hex '{hex_8_bit_str}' to Binary: {hexadecimal_to_binary(hex_8_bit_str)}")
	print(f"Binary '{binary_8_bit_str}' to Hex: {binary_to_hexadecimal(binary_8_bit_str)}")
	print(f"Binary '{binary_8_bit_str}' to Decimal: {binary_to_decimal(binary_8_bit_str)}")

	print("-" * 30)

	# 16-bit examples
	decimal_16_bit = 65435 # Max 16-bit unsigned
	hex_16_bit_str = "FFFF"
	binary_16_bit_str = "1111111111111111"

	print(f"Decimal {decimal_16_bit} to Hex: {decimal_to_hexadecimal(decimal_16_bit)}")
	print(f"Decimal {decimal_16_bit} to Binary: {decimal_to_binary(decimal_16_bit)}")
	print(f"Hex '{hex_16_bit_str}' to Decimal: {hexadecimal_to_decimal(hex_16_bit_str)}")
	print(f"Hex '{hex_16_bit_str}' to Binary: {hexadecimal_to_binary(hex_16_bit_str)}")
	print(f"Binary '{binary_16_bit_str}' to Hex: {binary_to_hexadecimal(binary_16_bit_str)}")
	print(f"Binary '{binary_16_bit_str}' to Decimal: {binary_to_decimal(binary_16_bit_str)}")
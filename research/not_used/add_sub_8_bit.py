def add_8bit(a, b):
	"""Adds two 8-bit integers and handles overflow."""
	
	print("a before: ", a)
	print("b before: ", b)

	# Ensure inputs are within the 8-bit range (0-255)
	a = a & 0xFF  # Bitwise AND to keep within 8 bits
	b = b & 0xFF

	print("a after: ", a)
	print("b after:", b)
	result = a + b

	# Check for overflow
	if result > 255:
		result = result & 0xFF #mask the result to 8 bits, effectively wrapping it.
		overflow = True
	else:
		overflow = False

	return result, overflow

def subtract_8bit(a, b):
	print("a before: ", a)
	print("b before: ", b)

	"""Subtracts two 8-bit integers and handles underflow."""
	a = a & 0xFF
	b = b & 0xFF

	print("a after: ", a)
	print("b after:", b)

	result = a - b

	if result < 0:
		result = result & 0xFF #mask to 8 bits, this will wrap around.
		underflow = True
	else:
		underflow = False

	return result, underflow

if __name__ == "__main__":
	
	# Example usage:
	num1 = 300
	num2 = 100

	print("Addition...")

	sum_result, overflow_flag = add_8bit(num1, num2)

	print("num1: ", num1, "\nnum2: ", num2)
	print(f"Sum: {sum_result}")
	print(f"Overflow: {overflow_flag}\n")

	# Example to demonstrate overflow
	num3 = 250
	num4 = 10

	print("Addition...")

	sum_result2, overflow_flag2 = add_8bit(num3, num4)

	print("num3: ", num3, "\nnum4: ", num4)
	print(f"Sum: {sum_result2}")
	print(f"Overflow: {overflow_flag2}\n")

	num5 = 125
	num6 = 200

	print("Subtraction...")

	sub_result, underflow_flag = subtract_8bit(num5, num6)

	print("num5: ", num5, "\nnum6: ", num6)
	print(f"Subtraction result: {sub_result}")
	print(f"Underflow: {underflow_flag}\n")

	num7 = 200
	num8 = 100

	print("Subtraction...")

	sub_result, underflow_flag = subtract_8bit(num7, num8)

	print("num7: ", num7, "\nnum8: ", num8)
	print(f"Subtraction result: {sub_result}")
	print(f"Underflow: {underflow_flag}\n")

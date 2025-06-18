def multiply_8bit(a, b):
	"""Adds two 8-bit integers and handles overflow."""
	
	print("a before: ", a)
	print("b before: ", b)

	# Ensure inputs are within the 8-bit range (0-255)
	a = a & 0xFF  # Bitwise AND to keep within 8 bits
	b = b & 0xFF

	print("a after: ", a)
	print("b after:", b)

	result = a * b

	# Check for overflow
	if result > 255:
		result = result & 0xFF #mask the result to 8 bits, effectively wrapping it.
		overflow = True
	else:
		overflow = False

	return result, overflow

def divide_8bit(a, b):
	print("a before: ", a)
	print("b before: ", b)

	"""Subtracts two 8-bit integers and handles underflow."""
	a = a & 0xFF
	b = b & 0xFF

	print("a after: ", a)
	print("b after:", b)

	if b == 0:
		return 0, 0, True

	quotient = a // b
	remainder = a % b

	if quotient > 255:
		overflow = True
		quotient = quotient & 0xFF
	else:
		overflow = False
	
	return quotient, remainder, overflow

if __name__ == "__main__":
	# Multiplication example
	num1 = 10
	num2 = 25
	product, overflow_mult = multiply_8bit(num1, num2)
	print(f"{num1} * {num2} = {product}, Overflow: {overflow_mult}")

	num3 = 20
	num4 = 20
	product2, overflow_mult2 = multiply_8bit(num3,num4)
	print(f"{num3} * {num4} = {product2}, Overflow: {overflow_mult2}")

	# Division example
	num5 = 100
	num6 = 7
	quotient, remainder, div_by_zero = divide_8bit(num5, num6)
	print(f"{num5} / {num6} = Quotient: {quotient}, Remainder: {remainder}, Division by zero: {div_by_zero}")

	num7 = 200
	num8 = 0
	quotient2, remainder2, div_by_zero2 = divide_8bit(num7, num8)
	print(f"{num7} / {num8} = Quotient: {quotient2}, Remainder: {remainder2}, Division by zero: {div_by_zero2}")

	num9 = 255
	num10 = 1
	quotient3, remainder3, overflow3 = divide_8bit(num9,num10)
	print(f"{num9} / {num10} = Quotient: {quotient3}, remainder: {remainder3}, overflow: {overflow3}")
	print("\n")
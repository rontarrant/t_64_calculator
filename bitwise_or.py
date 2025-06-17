'''
def bitwise_or(a: int, b: int) -> int:
	"""
	Perform bitwise OR operation on two signed integers.

	Args:
		a (int): First signed integer.
		b (int): Second signed integer.

	Returns:
		int: Result of bitwise OR operation.
	"""
	return a | b

if __name__ == "__main__":
	a = int(input("Enter a signed integer: "))
	b = int(input("Enter another signed integer: "))

	result = bitwise_or(a, b)
	print(f"bitwise_or({a}, {b}) = {result}")
'''

'''def to_32bit_binary(n: int) -> str:
    """
    Convert an integer to a 32-bit two's complement binary string.
    """
    return format(n & 0xFFFFFFFF, '032b')

def bitwise_or(a: int, b: int) -> int:
    """
    Perform bitwise OR operation on two signed integers.

    Args:
        a (int): First signed integer.
        b (int): Second signed integer.

    Returns:
        int: Result of bitwise OR operation.
    """
    return a | b

if __name__ == "__main__":
    a = int(input("Enter a signed integer: "))
    b = int(input("Enter another signed integer: "))

    result = bitwise_or(a, b)

    print(f"a in binary (32-bit two's complement): {to_32bit_binary(a)}")
    print(f"b in binary (32-bit two's complement): {to_32bit_binary(b)}")
    print(f"bitwise_or({a}, {b}) = {result}")
    print(f"Result in binary (32-bit two's complement): {to_32bit_binary(result)}")
'''

def to_8bit_binary(n: int) -> str:
    """
    Convert an integer to an 8-bit two's complement binary string.
    """
    return format(n & 0xFF, '08b')

def bitwise_or(a: int, b: int) -> int:
    """
    Perform bitwise OR operation on two signed integers.

    Args:
        a (int): First signed integer.
        b (int): Second signed integer.

    Returns:
        int: Result of bitwise OR operation.
    """
    return a | b

if __name__ == "__main__":
    a = int(input("Enter a signed integer: "))
    b = int(input("Enter another signed integer: "))

    result = bitwise_or(a, b)

    print(f"a in binary (8-bit two's complement): {to_8bit_binary(a)}")
    print(f"b in binary (8-bit two's complement): {to_8bit_binary(b)}")
    print(f"bitwise_or({a}, {b}) = {result}")
    print(f"Result in binary (8-bit two's complement): {to_8bit_binary(result)}")

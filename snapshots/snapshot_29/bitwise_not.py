def to_8bit_binary(n: int) -> str:
    """
    Convert an integer to an 8-bit two's complement binary string.
    """
    return format(n & 0xFF, '08b')

def bitwise_not_8bit(n: int) -> int:
    """
    Perform bitwise NOT operation on an 8-bit signed integer.

    Args:
        n (int): Signed integer input (will be treated as 8-bit).

    Returns:
        int: Result of bitwise NOT as signed 8-bit integer.
    """
    # Apply bitwise NOT and mask to 8 bits
    result = ~n & 0xFF

    # Convert back to signed 8-bit integer
    if result & 0x80:  # if sign bit is set
        result -= 0x100

    return result

if __name__ == "__main__":
    n = int(input("Enter a signed integer (will be treated as 8-bit): "))

    result = bitwise_not_8bit(n)

    print(f"Input in binary (8-bit two's complement): {to_8bit_binary(n)}")
    print(f"Bitwise NOT result (decimal): {result}")
    print(f"Bitwise NOT result in binary (8-bit two's complement): {to_8bit_binary(result)}")

'''
# Signed 8-bit NOT (from previous example)
def bitwise_not_signed(n: int) -> int:
    result = ~n & 0xFF
    if result & 0x80:
        result -= 0x100
    return result

# Unsigned 8-bit NOT
def bitwise_not_unsigned(n: int) -> int:
    return ~n & 0xFF  # No conversion needed

'''
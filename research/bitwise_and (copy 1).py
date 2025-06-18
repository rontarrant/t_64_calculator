def to_8bit_binary(n: int) -> str:
    """
    Convert an integer to an 8-bit two's complement binary string.
    """
    return format(n & 0xFF, '08b')

def bitwise_and(a: int, b: int) -> int:
    """
    Perform bitwise AND operation on two signed integers.

    Args:
        a (int): First signed integer.
        b (int): Second signed integer.

    Returns:
        int: Result of bitwise AND operation.
    """
    return a & b

if __name__ == "__main__":
    a = int(input("Enter a signed integer: "))
    b = int(input("Enter another signed integer: "))

    result = bitwise_and(a, b)

    print(f"a in binary (8-bit two's complement): {to_8bit_binary(a)}")
    print(f"b in binary (8-bit two's complement): {to_8bit_binary(b)}")
    print(f"bitwise_and({a}, {b}) = {result}")
    print(f"Result in binary (8-bit two's complement): {to_8bit_binary(result)}")

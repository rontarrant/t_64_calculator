def _to_twos_complement(value, bit_width):
    """
    Converts a Python integer to its two's complement representation
    within the specified bit_width.
    """
    if value >= 0:
        return value
    else:
        # For negative numbers, Python's int handles two's complement naturally
        # when performing bitwise operations if we ensure it's within the range.
        # This is primarily for conceptual understanding.
        # Actual bitwise ops in Python treat negative numbers as infinitely long
        # two's complement, so we'll often use masking to constrain.
        return value + (1 << bit_width)

def _from_twos_complement(value, bit_width):
    """
    Converts a two's complement representation back to a Python signed integer.
    """
    msb_mask = 1 << (bit_width - 1)
    if (value & msb_mask) != 0:  # If MSB is set, it's a negative number
        return value - (1 << bit_width)
    else:
        return value

def _normalize(value, bit_width):
    """
    Ensures the value is within the positive range [0, 2^bit_width - 1]
    for bitwise operations, then converts back to signed representation.
    """
    mask = (1 << bit_width) - 1
    normalized_value = value & mask
    return _from_twos_complement(normalized_value, bit_width)

# --- Bitwise Operation Functions ---

def bitwise_and_signed(a, b, bit_width):
    """
    Performs bitwise AND on two signed integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    # Treat inputs as unsigned for the actual bitwise operation, then normalize.
    mask = (1 << bit_width) - 1
    result = (a & mask) & (b & mask)
    return _normalize(result, bit_width), True

def bitwise_or_signed(a, b, bit_width):
    """
    Performs bitwise OR on two signed integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    result = (a & mask) | (b & mask)
    return _normalize(result, bit_width), True

def bitwise_xor_signed(a, b, bit_width):
    """
    Performs bitwise XOR on two signed integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    result = (a & mask) ^ (b & mask)
    return _normalize(result, bit_width), True

def bitwise_not_signed(a, bit_width):
    """
    Performs bitwise NOT (one's complement) on a signed integer
    within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    # Python's ~ operator works on arbitrary precision.
    # We need to mask the result to simulate fixed width.
    result = (~a) & mask
    return _normalize(result, bit_width), True

def shift_left_signed(a, shift_by, bit_width):
    """
    Performs a logical left shift on a signed integer.
    Zeros are shifted in from the right.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    if shift_by < 0:
        raise ValueError("Number of bits to shift must be non-negative")

    mask = (1 << bit_width) - 1
    # Perform the shift, then mask to truncate any overflow
    # and normalize to signed representation.
    shifted_val = (a & mask) << shift_by
    return _normalize(shifted_val, bit_width), True

def shift_right_signed(a, shift_by, bit_width):
    """
    Performs an arithmetic right shift on a signed integer.
    The sign bit is extended from the left.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    if shift_by < 0:
        raise ValueError("Number of bits to shift must be non-negative")

    # Python's default '>>' operator performs an arithmetic right shift
    # for its arbitrary-precision integers. We need to ensure we're
    # operating on the correctly signed representation within the fixed width.
    
    # First, convert 'a' to its true signed value within the bit_width if it's currently
    # represented by a positive masked value.
    actual_signed_a = _from_twos_complement(a & ((1 << bit_width) - 1), bit_width)

    # Perform the arithmetic shift using Python's '>>'
    shifted_val = actual_signed_a >> shift_by
    
    # Normalize the result back to the expected fixed-width signed representation
    return _normalize(shifted_val, bit_width), True


# --- Example Usage ---
if __name__ == "__main__":
    print("--- 8-bit Signed Examples ---")
    # 8-bit signed range: -128 to 127

    a_8 = 5       # 0000 0101
    b_8 = -10     # 1111 0110 (two's complement of 10)
    c_8 = 127     # 0111 1111
    d_8 = -128    # 1000 0000

    print(f"a_8 ({a_8}) = {bin(a_8 & 0xFF)[2:].zfill(8)}")
    print(f"b_8 ({b_8}) = {bin(b_8 & 0xFF)[2:].zfill(8)}")
    print(f"c_8 ({c_8}) = {bin(c_8 & 0xFF)[2:].zfill(8)}")
    print(f"d_8 ({d_8}) = {bin(d_8 & 0xFF)[2:].zfill(8)}\n")

    print(f"AND({a_8}, {b_8}): {bitwise_and_signed(a_8, b_8, 8)}") # Expected: 0 (0000 0000)
    print(f"OR({a_8}, {b_8}): {bitwise_or_signed(a_8, b_8, 8)}")   # Expected: -5 (1111 1011)
    print(f"XOR({a_8}, {b_8}): {bitwise_xor_signed(a_8, b_8, 8)}") # Expected: -5 (1111 1011)
    print(f"NOT({a_8}): {bitwise_not_signed(a_8, 8)}")             # Expected: -6 (1111 1010)
    print(f"NOT({b_8}): {bitwise_not_signed(b_8, 8)}")             # Expected: 9 (0000 1001)

    print(f"Shift Left ({a_8}, 1): {shift_left_signed(a_8, 1, 8)}")        # Expected: 10
    print(f"Shift Left ({c_8}, 1): {shift_left_signed(c_8, 1, 8)}")        # Expected: -2 (0111 1111 -> 1111 1110) - overflowed
    print(f"Shift Left ({d_8}, 1): {shift_left_signed(d_8, 1, 8)}")        # Expected: 0 (1000 0000 -> 0000 0000) - overflowed

    print(f"Shift Right Logical ({b_8}, 1): {shift_right_signed_logical(b_8, 1, 8)}") # Expected: 123 (1111 0110 -> 0111 1011) - zeros shifted in
    print(f"Shift Right Arithmetic ({b_8}, 1): {shift_right_signed(b_8, 1, 8)}") # Expected: -5 (1111 0110 -> 1111 1011) - sign bit extended
    print(f"Shift Right Logical ({c_8}, 1): {shift_right_signed_logical(c_8, 1, 8)}") # Expected: 63 (0111 1111 -> 0011 1111)
    print(f"Shift Right Arithmetic ({c_8}, 1): {shift_right_signed(c_8, 1, 8)}") # Expected: 63 (0111 1111 -> 0011 1111)

    print("\n--- 16-bit Signed Examples ---")
    # 16-bit signed range: -32768 to 32767

    a_16 = 256    # 0000 0001 0000 0000
    b_16 = -1     # 1111 1111 1111 1111
    c_16 = 32767  # 0111 1111 1111 1111
    d_16 = -32768 # 1000 0000 0000 0000

    print(f"AND({a_16}, {b_16}): {bitwise_and_signed(a_16, b_16, 16)}") # Expected: 256
    print(f"OR({a_16}, {b_16}): {bitwise_or_signed(a_16, b_16, 16)}")   # Expected: -1
    print(f"XOR({a_16}, {b_16}): {bitwise_xor_signed(a_16, b_16, 16)}") # Expected: -257
    print(f"NOT({a_16}): {bitwise_not_signed(a_16, 16)}")               # Expected: -257
    print(f"NOT({b_16}): {bitwise_not_signed(b_16, 16)}")               # Expected: 0

    print(f"Shift Left ({a_16}, 1): {shift_left_signed(a_16, 1, 16)}")        # Expected: 512
    print(f"Shift Left ({c_16}, 1): {shift_left_signed(c_16, 1, 16)}")        # Expected: -2 (0111... -> 1111...1110) - overflow
    print(f"Shift Left ({d_16}, 1): {shift_left_signed(d_16, 1, 16)}")        # Expected: 0 (1000... -> 0000...0000) - overflow

    print(f"Shift Right Logical ({b_16}, 1): {shift_right_signed_logical(b_16, 1, 16)}") # Expected: 32767
    print(f"Shift Right Arithmetic ({b_16}, 1): {shift_right_signed(b_16, 1, 16)}") # Expected: -1
    print(f"Shift Right Logical ({d_16}, 1): {shift_right_signed_logical(d_16, 1, 16)}") # Expected: 16384
    print(f"Shift Right Arithmetic ({d_16}, 1): {shift_right_signed(d_16, 1, 16)}") # Expected: -16384

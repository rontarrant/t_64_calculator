# --- Helper Function for Unsigned ---
def _normalize(value, bit_width):
    """
    Ensures the value stays within the unsigned range [0, 2^bit_width - 1].
    """
    mask = (1 << bit_width) - 1
    return value & mask

# --- Unsigned Bitwise Operation Functions ---

def bitwise_and(a, b, bit_width):
    """
    Performs bitwise AND on two unsigned integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    # Mask inputs to ensure they are treated as unsigned within the bit_width
    mask = (1 << bit_width) - 1
    result = (a & mask) & (b & mask)
    print("result: ", result)
    return result, True # No complex normalization needed, just masking

def bitwise_or(a, b, bit_width):
    """
    Performs bitwise OR on two unsigned integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    result = (a & mask) | (b & mask)
    return result

def bitwise_xor(a, b, bit_width):
    """
    Performs bitwise XOR on two unsigned integers within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    result = (a & mask) ^ (b & mask)
    return result, True

def bitwise_not(a, bit_width):
    """
    Performs bitwise NOT (one's complement) on an unsigned integer
    within the specified bit_width.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    mask = (1 << bit_width) - 1
    # Python's ~ operator works on arbitrary precision.
    # We need to mask the result to simulate fixed width.
    result = (~a) & mask
    return result, True

def shift_left(a, shift_by, bit_width):
    """
    Performs a logical left shift on an unsigned integer.
    Zeros are shifted in from the right.
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    if shift_by < 0:
        raise ValueError("Number of bits to shift must be non-negative")

    mask = (1 << bit_width) - 1
    # Perform the shift, then mask to truncate any overflow
    shifted_val = (a & mask) << shift_by
    return _normalize(shifted_val, bit_width), True

def shift_right(a, shift_by, bit_width):
    """
    Performs a logical right shift on an unsigned integer.
    Zeros are shifted in from the left. (Equivalent to logical_right_shift for signed)
    """
    if not (bit_width == 8 or bit_width == 16):
        raise ValueError("bit_width must be 8 or 16")

    if shift_by < 0:
        raise ValueError("Number of bits to shift must be non-negative")

    mask = (1 << bit_width) - 1
    # Ensure 'a' is treated as unsigned for the logical shift
    unsigned_a = a & mask
    shifted_val = unsigned_a >> shift_by
    return _normalize(shifted_val, bit_width), True


# --- Example Usage for Unsigned ---
if __name__ == "__main__":
    print("--- 8-bit Unsigned Examples ---")
    # 8-bit unsigned range: 0 to 255

    a_8u = 5      # 0000 0101
    b_8u = 246    # 1111 0110 (equivalent to -10 signed)
    c_8u = 127    # 0111 1111
    d_8u = 255    # 1111 1111 (equivalent to -1 signed)

    print(f"a_8u ({a_8u}) = {bin(a_8u & 0xFF)[2:].zfill(8)}")
    print(f"b_8u ({b_8u}) = {bin(b_8u & 0xFF)[2:].zfill(8)}")
    print(f"c_8u ({c_8u}) = {bin(c_8u & 0xFF)[2:].zfill(8)}")
    print(f"d_8u ({d_8u}) = {bin(d_8u & 0xFF)[2:].zfill(8)}\n")

    print(f"AND({a_8u}, {b_8u}): {bitwise_and(a_8u, b_8u, 8)}") # Expected: 4 (0000 0100)
    print(f"OR({a_8u}, {b_8u}): {bitwise_or(a_8u, b_8u, 8)}")   # Expected: 247 (1111 0111)
    print(f"XOR({a_8u}, {b_8u}): {bitwise_xor(a_8u, b_8u, 8)}") # Expected: 243 (1111 0011)
    print(f"NOT({a_8u}): {bitwise_not(a_8u, 8)}")             # Expected: 250 (1111 1010)
    print(f"NOT({d_8u}): {bitwise_not(d_8u, 8)}")             # Expected: 0 (0000 0000)

    print(f"Shift Left ({a_8u}, 1): {shift_left(a_8u, 1, 8)}")        # Expected: 10
    print(f"Shift Left ({c_8u}, 1): {shift_left(c_8u, 1, 8)}")        # Expected: 254 (0111 1111 -> 1111 1110)
    print(f"Shift Left ({d_8u}, 1): {shift_left(d_8u, 1, 8)}")        # Expected: 254 (1111 1111 -> 1111 1110)

    print(f"Shift Right ({b_8u}, 1): {shift_right(b_8u, 1, 8)}") # Expected: 123 (1111 0110 -> 0111 1011)
    print(f"Shift Right ({d_8u}, 1): {shift_right(d_8u, 1, 8)}") # Expected: 127 (1111 1111 -> 0111 1111)


    print("\n--- 16-bit Unsigned Examples ---")
    # 16-bit unsigned range: 0 to 65535

    a_16u = 256   # 0000 0001 0000 0000
    b_16u = 65535 # 1111 1111 1111 1111 (equivalent to -1 signed)
    c_16u = 32767 # 0111 1111 1111 1111
    d_16u = 32768 # 1000 0000 0000 0000 (equivalent to -32768 signed)

    print(f"AND({a_16u}, {b_16u}): {bitwise_and(a_16u, b_16u, 16)}") # Expected: 256
    print(f"OR({a_16u}, {b_16u}): {bitwise_or(a_16u, b_16u, 16)}")   # Expected: 65535
    print(f"XOR({a_16u}, {b_16u}): {bitwise_xor(a_16u, b_16u, 16)}") # Expected: 65279
    print(f"NOT({a_16u}): {bitwise_not(a_16u, 16)}")               # Expected: 65279
    print(f"NOT({b_16u}): {bitwise_not(b_16u, 16)}")               # Expected: 0

    print(f"Shift Left ({a_16u}, 1): {shift_left(a_16u, 1, 16)}")        # Expected: 512
    print(f"Shift Left ({c_16u}, 1): {shift_left(c_16u, 1, 16)}")        # Expected: 65534
    print(f"Shift Left ({d_16u}, 1): {shift_left(d_16u, 1, 16)}")        # Expected: 0 (overflow, all bits shifted out)

    print(f"Shift Right ({b_16u}, 1): {shift_right(b_16u, 1, 16)}") # Expected: 32767
    print(f"Shift Right ({d_16u}, 1): {shift_right(d_16u, 1, 16)}") # Expected: 16384
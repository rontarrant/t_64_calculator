# This is for correcting full_calculator_deepseek.py's set_base_mode()
def convert_base(number_str, input_base, output_base):
    """
    Converts a number from one base (binary, decimal, or hexadecimal)
    to another.

    Args:
        number_str (str): The number to convert, as a string.
        input_base (int): The base of the input number (2, 10, or 16).
        output_base (int): The desired base for the output number (2, 10, or 16).

    Returns:
        str: The converted number as a string in the output base.
             Returns an error message string if bases are invalid.
    """

    valid_bases = {2, 10, 16}

    if input_base not in valid_bases:
        return f"Error: Invalid input base. Must be 2, 10, or 16. Got {input_base}"
    if output_base not in valid_bases:
        return f"Error: Invalid output base. Must be 2, 10, or 16. Got {output_base}"
    if input_base == output_base:
        return number_str # No conversion needed if bases are the same

    try:
        # Step 1: Convert the input number to a base-10 integer
        decimal_value = int(number_str, input_base)

        # Step 2: Convert the base-10 integer to the desired output base
        if output_base == 10:
            return str(decimal_value)
        elif output_base == 16:
            # hex() returns '0x...'
            return hex(decimal_value)[2:]
        elif output_base == 2:
            # bin() returns '0b...'
            return bin(decimal_value)[2:]

    except ValueError:
        return f"Error: Invalid number string '{number_str}' for base {input_base}."
    except TypeError:
        return "Error: Number string must be a string."


# --- Examples ---

# Binary to Hexadecimal
print(f"Binary '1111' (decimal 15) to Hex: {convert_base('1111', 2, 16)}")
print(f"Binary '10101010' (decimal 170) to Hex: {convert_base('10101010', 2, 16)}")

# Binary to Decimal
print(f"Binary '1011' to Decimal: {convert_base('1011', 2, 10)}")

# Decimal to Binary
print(f"Decimal '15' to Binary: {convert_base('15', 10, 2)}")
print(f"Decimal '255' to Binary: {convert_base('255', 10, 2)}")

# Decimal to Hexadecimal
print(f"Decimal '255' to Hex: {convert_base('255', 10, 16)}")
print(f"Decimal '10' to Hex: {convert_base('10', 10, 16)}")

# Hexadecimal to Binary
print(f"Hex 'F' (decimal 15) to Binary: {convert_base('F', 16, 2)}")
print(f"Hex 'AA' (decimal 170) to Binary: {convert_base('AA', 16, 2)}")

# Hexadecimal to Decimal
print(f"Hex 'FF' to Decimal: {convert_base('FF', 16, 10)}")
print(f"Hex 'A' to Decimal: {convert_base('A', 16, 10)}")

# Negative numbers
print(f"Decimal '-10' to Hex: {convert_base('-10', 10, 16)}")
print(f"Hex '-a' to Decimal: {convert_base('-a', 16, 10)}")
print(f"Decimal '-10' to Binary: {convert_base('-10', 10, 2)}") # Note: Python's bin() shows negative as -0b...

# Error handling
print(f"Invalid input base: {convert_base('10', 5, 10)}")
print(f"Invalid output base: {convert_base('10', 10, 7)}")
print(f"Invalid number for base: {convert_base('abc', 2, 10)}")
print(f"Invalid number for base: {convert_base('2', 2, 10)}") # '2' is not valid in binary

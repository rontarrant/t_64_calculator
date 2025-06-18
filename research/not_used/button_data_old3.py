BUTTON_PATH = "button_images"

# Button image file names in the order they appear on the calculator window.
# Note: Any button that doesn't have an inactive state has the same
# image name for both active and inactive button versions.
# key: file name, value: [set name, in/active by default, callback name]
button_data: list[str, str, str, str] = [
	["numsys_hex",			"numsys",	"inactive",	"select_number_system"	],
	["digit_d",				"none",		"inactive",	"insert_d"					],
	["digit_e",				"none",		"inactive",	"insert_e"					],
	["digit_f",				"none",		"inactive",	"insert_f"					],
	["t64_logo",			"none",		"always",	"about"						],

	["numsys_dec",			"numsys",	"active",	"select_number_system"	],
	["digit_a",				"none",		"inactive",	"insert_a"					],
	["digit_b",				"none",		"inactive",	"insert_b"					],
	["digit_c",				"none",		"inactive",	"insert_c"					],
	["math_div",			"none",		"always",	"insert_division_sign"	],

	["numsys_oct",			"numsys",	"inactive",	"select_number_system"	],
	["digit_7",				"none",		"active",	"insert_7"					],
	["digit_8",				"none",		"active",	"insert_8"					],
	["digit_9",				"none",		"active",	"insert_9"					],
	["math_mult",			"none",		"always",	"insert_multiply_sign"	],

	["numsys_bin",			"numsys",	"inactive",	"select_number_system"	],
	["digit_4",				"none",   	"active",	"insert_4"					],
	["digit_5",				"none",  	"active",	"insert_5"					],
	["digit_6",				"none",   	"active",	"insert_6"					],
	["math_sub",			"none",  	"always",	"insert_subtract_sign"	],

	["bit_32",				"bits",		"inactive",	"select_bit_width"		],
	["digit_1",				"none",		"always",	"insert_1"					],
	["digit_2",				"none",		"active",	"insert_2"					],
	["digit_3",				"none",		"active",	"insert_3"					],
	["math_add",			"none",		"always",	"insert_addition_sign"	],

	["bit_16",				"bits",		"inactive",	"select_bit_width"		],
	["bracket_left",		"none",		"always",	"insert_left_bracket"	],
	["digit_0",				"none",		"always",	"insert_0"					],
	["dot",					"none",		"active",	"insert_dot"				],
	["bracket_right",		"none",		"always",	"insert_right_bracket"	],

	["bit_8",				"bits",		"active",	"select_bit_width"		],
	["signed",				"none",		"inactive",	"set_un_signed"			],
	["edit_clear",			"none",		"always",	"clear_display"			],
	["edit_backspace",	"none",		"always",	"do_backspace"				],
	["math_equals",		"none",		"always",	"do_math"					],
 ] # button_data

hex_inactive: list = [
	"dot",
]
dec_inactive: list = [
	"digit_a",
	"digit_b",
	"digit_c",
	"digit_d",
	"digit_e",
	"digit_f",
]
oct_inactive: list = [
	"digit_8",
	"digit_9",
	"digit_a",
	"digit_b",
	"digit_c",
	"digit_d",
	"digit_e",
	"digit_f",
	"dot"
]
bin_inactive: list = [
	"digit_2",
	"digit_3",
	"digit_4",
	"digit_5",
	"digit_6",
	"digit_7",
	"digit_8",
	"digit_9",
	"digit_a",
	"digit_b",
	"digit_c",
	"digit_d",
	"digit_e",
	"digit_f",
	"dot"
]
numsys_button_group: list = ["numsys_hex", "numsys_dec", "numsys_oct", "numsys_bin"]
bits_button_group: list = ["bit_8", "bit_16", "bit_32"]

bit_8_unsigned_range = range(0, 255)
bit_8_signed_range = range(-128, 127)
bit_16_unsigned_range = range(0, 65535)
bit_16_signed_range = range(-32768, 32767)
bit_32_unsigned_range = range(0, 4294967295)
bit_32_signed_range = range(-2147483648, 2147483647)

modes: list = [
	"hex_8_bit_signed",
	"hex_8_bit_unsigned",
	"hex_16_bit_signed",
	"hex_16_bit_unsigned",
	"hex_32_bit_signed",
	"hex_32_bit_unsigned",
	"dec_8_bit_signed",
	"dec_8_bit_unsigned",
	"dec_16_bit_signed",
	"dec_16_bit_unsigned",
	"dec_32_bit_signed",
	"dec_32_bit_unsigned",
	"oct_8_bit_signed",
	"oct_8_bit_unsigned",
	"oct_16_bit_signed",
	"oct_16_bit_unsigned",
	"oct_32_bit_signed",
	"oct_32_bit_unsigned",
	"bin_8_bit_signed",
	"bin_8_bit_unsigned",
	"bin_16_bit_signed",
	"bin_16_bit_unsigned",
	"bin_32_bit_signed",
	"bin_32_bit_unsigned",
]

if __name__ == "__main__":
	for key, value in button_data.items():
		print(f"Key: {key}") # see list of file names
		print("\t", value[0], ", ", value[1]) # see individual file names

	print("buttons that are inactive by default:")
	for string in button_data:
		print(string)

# PySide6
from PySide6.QtGui import QColor

# Python: make the C64Palette class immutable
from dataclasses import dataclass

'''
The Commodore C-64 Palette

This class is designed to be immutable and so
doesn't need to be instantiated. Don't forget the
brackets before the dot.

To retrieve a colour:
	my_colour = C64Palette().red

To retrieve a palette:
	my_palette = C64Palette().bits
'''
@dataclass(frozen = True)
class C64Palette:
	# Pre-defined colours based on the palette
	# available on the original Commodore C-64.
	shadow_colour = QColor(0, 0, 0, 80)
	black = QColor("#000000")
	white = QColor("#FFFFFF")
	red = QColor("#880000")
	cyan = QColor("#AAFFEE")
	violet = QColor("#CC44CC")
	green = QColor("#00CC55")
	blue = QColor("#0000AA")
	yellow = QColor("#EEEE77")
	orange = QColor("#DD8855")
	brown = QColor("#664400")
	light_red = QColor("#FF7777")
	dark_grey= QColor("#333333")
	medium_grey = QColor("#777777")
	light_green = QColor("#AAFF66")
	light_blue = QColor("#0088FF")
	light_grey = QColor("#BBBBBB")

	# Pre-defined palettes for the T-64 Calculator
	numsys = {"bg": red, "font": yellow, "outline": dark_grey}
	bits = {"bg": cyan, "font": blue, "outline": blue}
	dark = {"bg": medium_grey, "font": light_grey, "outline": dark_grey}
	digit = {"bg": yellow, "font": red, "outline": light_red}
	light = {"bg": light_grey, "font": medium_grey, "outline": medium_grey}
	math = {"bg": light_red, "font": red, "outline": red}
	edit = {"bg": light_green, "font": blue, "outline": blue}
	about = {"bg": yellow, "font": red, "outline": blue}

'''
Test
'''
if __name__ == "__main__":
	numsys_palette = C64Palette().numsys
	bits_palette = C64Palette().bits
	digit_palette = C64Palette().digit
	my_colour01 = C64Palette().red
	my_colour02 = C64Palette().green

	print("numsys:")

	for key, value in numsys_palette.items():
		print(key, ": ", value)
	
	print("\nbits:")

	for key, value in bits_palette.items():
		print(key, ": ", value)

	print("\ndigit:")

	for key, value in digit_palette.items():
		print(key, ": ", value)

	print()
	print("my_colour01: ", my_colour01)
	print("my_colour02: ", my_colour02)
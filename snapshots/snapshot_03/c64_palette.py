from PySide6.QtGui import QColor

class C64Palette:
	shadow_color = QColor(0, 0, 0, 80)
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

	numsys = {"bg": red, "font": yellow, "outline": dark_grey}
	dark_inactive = {"bg": medium_grey, "font": light_grey, "outline": dark_grey}
	bits = {"bg": light_blue, "font": blue, "outline": blue}
	digit = {"bg": yellow, "font": red, "outline": light_red}
	light_inactive = {"bg": light_grey, "font": medium_grey, "outline": medium_grey}
	math = {"bg": light_red, "font": red, "outline": red}
	edit = {"bg": light_green, "font": blue, "outline": blue}
	about = {"bg": yellow, "font": red, "outline": blue}

	def get(self, group_name):
		match group_name:
			case "numsys":
				palette = self.numsys
			case "bits":
				palette = self.bits
			case "dark":
				palette = self.dark_inactive
			case "digit":
				palette = self.digit
			case "light":
				palette = self.light_inactive
			case "math":
				palette = self.math
			case "edit":
				palette = self.edit
			case "about":
				palette = self.about
		
		return palette
	
if __name__ == "__main__":
	numsys_palette = C64Palette().get("numsys")
	bits_palette = C64Palette().get("bits")
	digit_palette = C64Palette().get("digit")

	print("numsys:")
	for key, value in numsys_palette.items():
		print(key, ": ", value)
	
	print("\nbits:")

	for key, value in bits_palette.items():
		print(key, ": ", value)

	print("\ndigit:")

	for key, value in digit_palette.items():
		print(key, ": ", value)

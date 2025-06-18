from PySide6.QtGui import QColor
from c64_palette import C64Palette

# specifications used for all buttons except Equals
base_specs = {
	"width": 120,
	"height": 80,
	"outline": 4,
	"radius": 15,
	"font": "Arial Black",
	"shadow_colour": QColor(0, 0, 0, 50),
}

# OneLineButton's have their own font size
one_line_specs = base_specs.copy()
one_line_specs["font_size"] = 30

# TwoLineButton's have separate font sizes
# for each line of text
two_line_specs = base_specs.copy()
two_line_specs["font_size"] = 20
two_line_specs["subfont_size"] = 10

# AngledButton (there's only one) has its own font size
# as well as an angle for the text's baseline
angled_specs = base_specs.copy()
angled_specs["font_size"] = 26
angled_specs["angle"] = -30

# Equals: the only button with a unique width
equals_specs = base_specs.copy()
equals_specs["width"] = base_specs["width"] * 3 + 10
equals_specs["font_size"] = 30

# Set style sheets for wider borders
border_width = "4px"  # Adjust the width as needed
border_style = "solid"
border_color = "#000000"  # Can't use C64Palette here
border_radius = "10px"  # Adjust the radius for more or less rounded corners

input_style_sheet = f"border: {border_width} {border_style} {border_color}; border-radius: {border_radius};"

# Set a maximum width for the input and result widgets
max_input_width = 420  # A nod to my hippy days

lineedit_properties = {
	"width": 300,
	"height": 80,
	"radius": 15,
	"font": "Arial Black",
	"font_size": 30,
	"font_factor": 0.5,
	"text": "",
	"palette": {
			"bg": C64Palette().yellow,  # Blue
			"outline": C64Palette().blue,
			"text": C64Palette().blue,
	},
	"inactive_palette": {
			"bg": C64Palette().medium_grey,
			"outline": C64Palette().light_grey,
			"text": C64Palette().dark_grey
	},
	"specs": 
	{
			"outline": 4
	}
}
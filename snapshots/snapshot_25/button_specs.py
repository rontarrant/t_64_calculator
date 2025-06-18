from c64_palette import C64Palette

# scaling for UI
scale_factor = 0.6

# Common
master_radius = 15 * scale_factor
master_outline = 4 * scale_factor
font_factor = 0.5 * scale_factor

# Buttons
minimum_width = 60 * scale_factor
minimum_height = 40 * scale_factor
margin_pad_x = 20 * scale_factor
margin_pad_y = 40 * scale_factor
button_width = 120 * scale_factor
button_height = 80 * scale_factor
button_offset = 5 * scale_factor

# multi-column widgets
multi_column_pad_x = 10 * scale_factor
column_span = 3 * scale_factor

# button fonts
baseline_offset = 10 * scale_factor
minimum_font_size = 6 * scale_factor
one_line_size = 30 * scale_factor
two_line_size = 26 * scale_factor
two_line_sub_size = 14 * scale_factor
font_angle = -30 * scale_factor

# Labels
label_margin_left = 8 * scale_factor
label_margin_right = 16 * scale_factor
label_height = 70 * scale_factor

# specifications used for all buttons except Equals
base_specs = \
{
	"width": button_width,
	"height": button_height,
	"outline": master_outline,
	"offset": button_offset, # offset for animation
	"radius": master_radius,
	"font": "Arial Black",
	"font_factor": font_factor,
}

# OneLineButton's have their own font size
one_line_specs = base_specs.copy()
one_line_specs["font_size"] = one_line_size

# TwoLineButton's have separate font sizes
# for each line of text
two_line_specs = base_specs.copy()
two_line_specs["font_size"] = two_line_size
two_line_specs["subfont_size"] = two_line_sub_size

# AngledButton (there's only one) has its own font size
# as well as an angle for the text's baseline
angled_specs = base_specs.copy()
angled_specs["font_size"] = two_line_size
angled_specs["angle"] = font_angle

# Equals: the only button with a unique width
equals_specs = base_specs.copy()
equals_specs["width"] = base_specs["width"] * column_span + multi_column_pad_x
equals_specs["font_size"] = two_line_size

# Control sizes in LineEditColourLabel (fake QLineEdit)
lineedit_properties = \
{
	"width": equals_specs["width"],
	"height": label_height,
	"radius": master_radius,
	"font": "Arial Black",
	"font_size": one_line_size,
	"font_factor": font_factor,
	"text": "",
	"palette": 
	{
			"bg": C64Palette().yellow,  # Blue
			"outline": C64Palette().blue,
			"text": C64Palette().blue,
	},
	"inactive_palette": 
	{
			"bg": C64Palette().medium_grey,
			"outline": C64Palette().light_grey,
			"text": C64Palette().dark_grey
	},
	"specs": 
	{
			"outline": master_outline
	}
}
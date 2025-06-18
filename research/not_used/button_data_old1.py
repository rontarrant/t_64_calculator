from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class CalcButton(QPushButton):
   def __init__(self, properties):
      super().__init__()
      # common to all CalcButtons
      id = properties.id
      self.up_image = properties.up_image
      self.down_image = properties.down_image
   
   def callback(self):
      pass
      # use the id to do what needs doing

button_image_path = "./images"

button0 = ["0", "button_0_up.png", "button_0_down.png"]
button1 = ["1", "button_1_up.png", "button_1_down.png"]
button2 = ["2", "button_2_up.png", "button_2_down.png"]
button3 = ["3", "button_3_up.png", "button_3_down.png"]
button4 = ["4", "button_4_up.png", "button_4_down.png"]
button5 = ["5", "button_5_up.png", "button_5_down.png"]
button6 = ["6", "button_6_up.png", "button_6_down.png"]
button7 = ["7", "button_7_up.png", "button_7_down.png"]
button8 = ["8", "button_8_up.png", "button_8_down.png"]
button9 = ["9", "button_9_up.png", "button_9_down.png"]
buttona = ["a", "button_a_up.png", "button_a_down.png"]
buttonb = ["b", "button_b_up.png", "button_b_down.png"]
buttonc = ["c", "button_c_up.png", "button_c_down.png"]
buttond = ["d", "button_d_up.png", "button_d_down.png"]
buttone = ["e", "button_e_up.png", "button_e_down.png"]
buttonf = ["f", "button_f_up.png", "button_f_down.png"]

buttonadd = ["add", "button_add_up.png", "button_add_down.png"]
buttonsub = ["sub", "button_sub_up.png", "button_sub_down.png"]
buttonmult = ["mult", "button_mult_up.png", "button_mult_down.png"]
buttondiv = ["div", "button_div_up.png", "button_div_down.png"]
buttonequals = ["equals", "button_equals_up.png", "button_equals_down.png"]
button8bit = ["8bit", "button_8bit_up.png", "button_8bit_down.png"]
button16bit = ["16bit", "button_16bit_up.png", "button_16bit_down.png"]
button32bit = ["32bit", "button_32bit_up.png", "button_32bit_down.png"]
button64bit = ["64bit", "button_64bit_up.png", "button_64bit_down.png"]
buttonback = ["back", "button_back_up.png", "button_back_down.png"]
buttonclear = ["clear", "button_clear_up.png", "button_clear_down.png"]
buttondot = ["dot", "button_dot_up.png", "button_dot_down.png"]
buttonsigned = ["signed", "button_signed_on.png", "button_signed_off.png"]

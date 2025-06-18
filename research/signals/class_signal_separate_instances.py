# proof that each instance of a class gets its own
# instance of a class variable.
from PySide6.QtCore import QObject, Signal, Qt, Slot

class Test(QObject): # All Qt widgets inherit QObject.
	custom_signal = Signal(str)

	@Slot(str)
	def internal_slot(self, string):
		print('internal_slot...', string, self.message)

	def __init__(self, message):
		super().__init__()
		self.custom_signal.connect(self.internal_slot)
		self.message = message


test = Test("firing 1")
test2 = Test("firing 2")
test3 = Test('firing 3')

# first emission
test.custom_signal.emit("fire 1: ")

# 
test2.custom_signal.emit("fire 2: ")

test3.custom_signal.emit("fire 3: ")

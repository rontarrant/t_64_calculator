from PySide6.QtCore import QObject, Signal, Qt, Slot

class Test(QObject): # All Qt widgets inherit QObject.
	# Define a signal that emits a string.
	custom_signal = Signal(str)
    
	# Define a slot, internal to a class,
	# that accepts a string.
	@Slot(str)
	def internal_slot(self, string):
		print('internal_slot', string)

# Define another slot, but this one external
# to a class, that also accepts a string.      
@Slot(str)
def external_slot(string):
	print('external_slot', string)


test = Test()
test2 = Test()

# connect first signal to external slot
print("connect test signal to external slot:")
test.custom_signal.connect(external_slot)

# first emission
print("fire 1:")
test.custom_signal.emit("fire 1")

# connect second signal to internal slot
print("connect test's signal to its own internal slot:")
test.custom_signal.connect(test.internal_slot, type = Qt.ConnectionType.AutoConnection)

print("fire 2:")
test.custom_signal.emit("fire 2")
# connect first signal to the internal slot of the second object
print("connect test's signal to test2's internal slot:")
test.custom_signal.connect(test2.internal_slot)

# 
print("fire 3:")
test.custom_signal.emit("fire 3")

print("disconnect test's signal from external slot:")
test.custom_signal.disconnect(external_slot)

print("disconnect test's signal from test2's internal slot:")
test.custom_signal.disconnect(test2.internal_slot)

print("fire 4:")
test.custom_signal.emit("fire 4")

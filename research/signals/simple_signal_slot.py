from PySide6.QtCore import QObject, Signal, Qt, Slot

class Test(QObject): # All Qt widgets inherit QObject.
	custom_signal = Signal(str)
    
	@Slot(str)
	def internal_slot(self, string):
		print('internal_slot', string)
        
@Slot(str)
def external_slot(string):
	print('external_slot', string)


test = Test()

# connect first signal to external slot
print("connect signal to external slot:")
test.custom_signal.connect(external_slot)

# first emission
print("fire 1:")
test.custom_signal.emit("fire 1")

# connect second signal to internal slot
print("connect signal to internal slot:")
test.custom_signal.connect(test.internal_slot, type = Qt.ConnectionType.AutoConnection)

# 
print("fire 2:")
test.custom_signal.emit("fire 2")

print("disconnect signal from external slot:")
test.custom_signal.disconnect(external_slot)

print("fire 3:")
test.custom_signal.emit("fire 3")

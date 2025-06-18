class MyObject:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

my_dict = {"apple": 10, "banana": 20, "cherry": 30}
obj = MyObject(my_dict)

print(obj.apple)  # Output: 10
print(obj.banana) # output: 20
print(obj.cherry) # output: 30

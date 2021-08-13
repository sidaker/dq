class Shirt():
    def __init__(self,s_col,s_size,s_style,s_price):
        self.color = s_col
        self.size  = s_size
        self.style = s_style
        self.price = s_price

    def set_price(self,new_price):
        self.price = new_price

    def discount(self,disc):
        return  self.price * (1- disc)


## think self is special dictionary.

louisvetton_shirt = Shirt('red','S','short sleeve', 15)
print(louisvetton_shirt.color)
print(louisvetton_shirt.size)
print(louisvetton_shirt.style)
print(louisvetton_shirt.price)

'''
A function and a method look very similar.
They both use the def keyword. They also have inputs and return outputs.
The difference is that a method is inside of a class whereas a function is outside of a class.
'''

louisvetton_shirt.set_price(10)
print(louisvetton_shirt.discount(0.2))
print(louisvetton_shirt.price)

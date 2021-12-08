def raise_to(exp):
    # local function raise_to_exp
    def raise_to_exp(x):
        return pow(x, exp)
    return raise_to_exp

square = raise_to(2)
print(square.__closure__ )
print(square(5))
print(square(9))

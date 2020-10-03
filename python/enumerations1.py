from enum import Enum, unique , auto

@unique
class Fruits(Enum):
    APPLE = 1
    BANANA = 2
    ORANGE = 3
    PAPAYA = 4
    PEAR = auto()

def main():
    print(Fruits.APPLE)
    print(type(Fruits.APPLE))
    print(repr(Fruits.APPLE))
    print(Fruits.APPLE.name)
    print(Fruits.APPLE.value)
    print(Fruits.PEAR.name)
    print(Fruits.PEAR.value)

if __name__ == '__main__':
    main()

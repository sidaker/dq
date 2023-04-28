x = 0

match x:
    case 0:
       print("The zero case matches")
    case 1:
        print("one")
    case None:
        print("Norhing")

operations = [
    ["add", 1,2,3,4],
    ["mul",11,2],
    ["add",1,2]
]

for ops in operations:
    match ops:
        case "add", *nums:
            result = sum(nums)
            print(result)
        case "mul", num1. num2:
            result = num1 * num2
            print(result)
        case _:
            continue

print(sum([1,2,34,5]))



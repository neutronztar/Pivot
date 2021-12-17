def smart_add(num1, num2):
    sum = num1 + num2
    while sum >= 360:
        sum -= 360
    return sum

print(smart_add(350, 300000))
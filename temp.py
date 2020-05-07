def maxdiv2(digit):
    digit1 = digit
    while digit1 > 0:
        if not (digit % digit1 or digit1 & (digit1 - 1)):
            return digit1
        digit1 -= 1

print(maxdiv2(10))
print(maxdiv2(16))
print(maxdiv2(12))
print(maxdiv2(17))
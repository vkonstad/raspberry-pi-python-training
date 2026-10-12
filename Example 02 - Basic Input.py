# Example 02 - Basic Input
# Reads numbers from the keyboard until a non-number is entered
# (just press Enter on an empty line), then prints their sum.
#
# Concepts: variables, while loop, input(), type conversion, try/except

total = 0   # not called "sum", so we don't hide Python's built-in sum()

while True:
    text = input("New Value (empty line to finish): ")
    try:
        total += int(text)
    except ValueError:      # int() fails for text that is not a whole number
        break

print('Sum is', total)

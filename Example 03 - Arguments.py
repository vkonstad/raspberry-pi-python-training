# Example 03 - Arguments
# Sums the integer arguments given on the command line.
# Run:  python "Example 03 - Arguments.py" 10 20 abc 30
#
# Concepts: sys.argv, for loop, slicing, try/except

import sys

# sys.argv[0] is the name of the script itself, the real arguments start at [1]
args = sys.argv[1:]
print("Total arguments passed:", len(args))

total = 0

for arg in args:
    print('Argument', arg)
    try:
        total += int(arg)
    except ValueError:
        print('  (not a number, ignored)')

print('Sum is', total)

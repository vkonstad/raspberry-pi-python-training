# Example 07 - Simple timing
# Sums the numbers 0..n and measures how long it takes.
# Run:  python "Example 07 - Simple timing.py" 1000000
# Try it on a PC and on the Pi, and with different values of n.
#
# Concepts: functions, time.perf_counter(), comparing a loop with a formula

import sys, time


def sumTo(n):
    total = 0
    for i in range(0, n + 1):
        total += i
    return total


if len(sys.argv) < 2:
    print("Usage: python \"Example 07 - Simple timing.py\" <n>")
    sys.exit(1)

n = int(sys.argv[1])

start = time.perf_counter()
print(sumTo(n))
stop = time.perf_counter()
print("Loop:    ", round((stop - start) * 10**3, 3), "ms")

# The same result with a mathematical formula: no loop at all
start = time.perf_counter()
print(n * (n + 1) // 2)
stop = time.perf_counter()
print("Formula: ", round((stop - start) * 10**3, 3), "ms")

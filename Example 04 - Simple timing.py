import sys, pandas as pd, time

start = time.time()

def sumTo(n):
    sum = 0
    for i in range(0,int(n) + 1):
        sum += i
    return sum    

n = len(sys.argv)
print("Total arguments passed:", n)

print(sumTo(sys.argv[1]))

stop = time.time()

print("The time of execution of above program is :", (stop-start) * 10**3, "ms")
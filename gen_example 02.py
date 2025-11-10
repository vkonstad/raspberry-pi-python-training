import sys

n = len(sys.argv)
print("Total arguments passed:", n)

cont = True
sum = 0

for i in sys.argv:
    try:
        print('\nArgument ', i)
        sum += int(i)
    except:
        pass

print ('Sum is', sum)
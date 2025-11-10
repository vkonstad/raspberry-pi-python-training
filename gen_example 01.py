cont = True
sum = 0
while cont:
    try:
        x = input("New Value: ")
        sum += int(x)
    except: cont = False

print ('Sum is', sum)
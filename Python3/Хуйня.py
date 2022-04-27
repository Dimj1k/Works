k = []
maximums = []
minimums = []
with open('d', 'r') as file:
    for line in file:
        line = line.strip().split(" ")
        if int(line[0]) % 2 != 0: k.append([int(line[0]), int(line[1])])
    for i in k:
        maximums.append(max(i))
        minimums.append(min(i))
    maximum = sum(maximums)
    while maximum % 2 != 0:
        maximum -= min(maximums)
        maximums.remove(min(maximums))
    minimum = sum(maximums)
    while minimum % 2 == 0:
        minimum -= max(minimums)
        minimums.remove(max(minimums))
    print("Сумма больших чисел:", maximum, "\nСумма меньших чисел:", minimum)

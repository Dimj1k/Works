import datetime as dt
import time


dates = []
copies = []
ages = []
i = 0


with open('Auto.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        fio, date = line.split(':')
        if '\n' in date:
            date = date[0:date.find('\n')]
        if not '\t' in date:
            dates.append(date)
        else:
            dates.append('2.1.1970')
        copies.append(line.split('\n')[0])


for i in range(len(dates)):
    day, month, year = dates[i].split('.')
    if int(year) < 1970:
        year = (1969 - int(year)) + 1970
        age = int(((time.time() - 6 * 3600) + time.mktime(dt.date(int(year), int(month), int(day)).timetuple()))
                  / (365.25 * 86400))
    else:
        age = int(((time.time() - 6 * 3600) - time.mktime(dt.date(int(year), int(month), int(day)).timetuple()))
                  / (365.25 * 86400))
    ages.append(age)


with open('Auto.txt', 'w', encoding='UTF-8') as f:
    for i in range(len(copies)):
        if not '\t' in copies[i]:
            f.writelines([copies[i], '\t', str(ages[i])+' лет', '\n'])
        else:
            f.writelines([copies[i], '\n'])

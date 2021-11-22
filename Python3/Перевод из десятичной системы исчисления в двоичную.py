# Решение проблемы Python с помощью обычного округления чисел
def zn(x):
	qw=str(x)
	if '.' in qw:
		return abs(qw.find('.') - len(qw))-1
	else:
		return 0


n=float(input())
wt=zn(n)
n1=n-n//1
n=int(n)
k=''
p=[]
F=0
o1=0
o2=0


# Десятичные числа без плавающей точки
if n >= 1:
	while n >= 1:
		k=k+str(n%2)
		n=n//2
else:
	k='0'
k=k[::-1]
we=len(k)


# Десятичные числа с плавающей точкой
if n1 > 0:
    while F!=1:
	if wt < 16:
        	n1=round(n1,wt)
        p.append(n1)
        n1=n1*2
        if n1 >= 1:
            k=k+'1'
            n1=n1-1
        else: k=k+'0'
        j=len(p)
        ji=len(set(p))
        if j != ji:
            for i in range(0,j-1):
                F=1
                if p[i]==p[j-1]:
                    o1=i
                    o2=j-1


# Вывод десятичного числа в двоичную систему исчисления
if o1 > 0 or o2 > 0:
	o1=o1+we
	o2=o2+we
	if n1 != 0:
	    print(k[0:we]+'.'+k[we:o1]+'('+k[o1:o2]+')')
	else:
	    print(k[0:we]+'.'+k[we:o1])
else:
	print(k)

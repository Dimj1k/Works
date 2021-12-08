from decimal import Decimal, getcontext
n=float(input())
getcontext().prec = 16
n = Decimal(n)
n1=n-n//1
n=int(n)
k=''
p=[]
F=0
o1=0
o2=0
if n >= 1:
	while n >= 1:
		k=k+str(n%2)
		n=n//2
else:
	k='0'
k=k[::-1]
we=len(k)
if n1 > 0:
    while F!=1:
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
if o1 > 0 or o2 > 0:
	o1=o1+we
	o2=o2+we
	if n1 != 0:
	    print(k[0:we]+'.'+k[we:o1]+'('+k[o1:o2]+')')
	else:
	    print(k[0:we]+'.'+k[we:o1])
else:
	print(k)

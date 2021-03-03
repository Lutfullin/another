
#умная версия
import math

n = 10
m = 4
u = 70

p = (1/m)
k= int(n*(u/100))

result = 0

def f (number):
    return math.factorial(number)

for i in range(k,n):
    ni = f(n) / (f(n-i)*f(i))
    result +=  ni * (p**i) *  ((1-p)**(n-i)) 
    

print (round(result*100,2))


#мудацкая версия
import random



tests = []

peop = 10
for i in range(1,peop):
    test = 0
    for question in range(1,10):
        if (random.randint(1,4)==1):
            test += 1
    tests.append(test)
    print (i)    

good = 0
for i in tests:
    if (i>=7):
        good += 1

print ((good/peop)*100)

### Uses python3
### LCM
### LCM = (a*b) / (GCD)

def gcdEffi(a, b):
 if (a < b):
    a,b = b,a
 if (a == 1 and b == 1):
    gcd = 1
    return gcd
 elif (b == 0 and a != 0):
        gcd = a
        return gcd
 else:
    remainder = a%b 
    return gcdEffi(remainder,b)

a, b = map(int, input().split())
print(int((a*b) // gcdEffi(a, b)))
### Uses python3
### GCD

def gcdEffi(a, b):
 if (a < b):
    a,b = b,a
 if a == 0 and b == 0:
    gcd = 0
    return gcd
 elif b == 0 and a != 0:
        gcd = a
        return gcd
 else:
    remainder = a%b 
    return gcdEffi(remainder,b)

a, b = map(int, input().split())
print(gcdEffi(a, b))
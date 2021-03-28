# Uses python3
### LAST DIGIT FIBONACCI
# The n in the for loop is just a counter that iterates n-1 times + the element from outside 
# n-1+1 = n. That explains why iterating n-1 times returns Fibo(n)

def fibo(n):
    ### Fib Series = 0,1,1,2,3,5,8,13
 a = 0 # Not the first element, but rather the 2nd
 b = 1 # The 3rd element
 result = 0

 if  (n==0):
    return result  
 else:
        result = 1
        for i in range(1,n):
            result = a%10 + b%10
            a = b%10
            b = result%10
        return result % 10
                    
n = int(input())
print(fibo(n))
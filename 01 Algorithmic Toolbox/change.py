#### Uses python3
### RETURN CHANGE
### Returns the minimum number of coins to change 
### an amount of money X into coins of 1,5,10

def change(m):
    tenCoins, fiveCoins, oneCoins = 0 , 0, 0
    if (m>=10):
        tenCoins = m//10
        m = m - tenCoins*10
    if (m>=5):
        fiveCoins = m//5
        m = m - fiveCoins*5
    if (m>=1):
        oneCoins = m
        m = m - oneCoins        
    return int((tenCoins + fiveCoins + oneCoins))

m = int(input())
print(change(m))
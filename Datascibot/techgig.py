def main(str1, str2):
    m = len(str1)
    n = len(str2)
    j = 0 
    i = 0 
    while j < m and i < n:
        if str1[j] == str2[i]:
            j = j+1
        i = i + 1
    return j == m
str2 = str(input())
N = int(input())
for i in range(N):
    str1 = str(input())
    if main(str1, str2):
        print("POSITIVE") 
    else:
        print( "NEGATIVE")


def main():
    testCase = int(input())
    def isprime(n):
        if n<=1:
            return False
        for i in range(2,n):
            if n%i ==0:
                return False
        return True
    
    while testCase >0:
        LR = list(map(int,input().strip().split()))
        first = LR[0]
        last = LR[1]
        f = 0
        l = 0
        for i in range(first,last+1):
            if f ==0:
                if isprime(i):
                    f=i
                else:
                    i = i+1
            if l==0:
                if isprime(last):
                    l=last
                else:
                    last -=1
            if f!=0 and l!=0:
                break
            
        if f!=0 and l!=0:
            print(l-f)
        else:
            print(-1)
        
        testCase -=1

main()
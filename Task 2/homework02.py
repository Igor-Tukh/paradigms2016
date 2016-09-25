import numpy
from math import log2

def strassen(a, b):
    if a.shape[0] == 1:
        return numpy.array([a[0][0] * b[0][0]])
    
    mid = a.shape[0] // 2
    
    a11 = a[:mid, :mid]
    a12 = a[:mid, mid:]
    a21 = a[mid:, :mid]
    a22 = a[mid:, mid:]
    
    b11 = b[:mid, :mid]
    b12 = b[:mid, mid:]
    b21 = b[mid:, :mid]
    b22 = b[mid:, mid:]
    
    s1 = strassen(a11 + a22, b11 + b22)
    s2 = strassen(a21 + a22, b11)
    s3 = strassen(a11, b12 - b22)
    s4 = strassen(a22, b21 - b11)
    s5 = strassen(a11 + a12, b22)
    s6 = strassen(a21 - a11, b11 + b12)
    s7 = strassen(a12 - a22, b21 + b22)
    
    ans = numpy.zeros( (2 * mid, 2 * mid), dtype = 'int')
    
    ans[:mid, :mid] = s1 + s4 - s5 + s7
    ans[mid:, :mid] = s2 + s4
    ans[:mid, mid:] = s3 + s5
    ans[mid:, mid:] = s1 + s3 - s2 + s6
    
    return ans
    
      

if __name__ == "__main__":
    n = int(input())
    
    pow2 = 1 << (int(log2(n)))
    if (pow2 < n): pow2 *= 2
    first = numpy.zeros( (pow2, pow2), dtype = 'int')
    second = numpy.zeros(( pow2, pow2), dtype = 'int')
    
    for i in range(n):
        val = numpy.array(list(map(int, input().split())))
        first[i][0:n]=val.copy()
    
    for i in range(n):
        val = numpy.array(list(map(int, input().split())))
        second[i][0:n]=val.copy()
    
    ans = strassen(first, second)
    
    print("\nResult of multiplication:\n")
    for l in ans[:n]:
        print(' '.join(map(str, l[:n])))

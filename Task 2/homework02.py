import numpy
import sys
from math import log2, ceil

def strassen(a, b):
    if a.shape[0] == 1:
        return a * b
    
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
    
    ans = numpy.zeros( (2 * mid, 2 * mid), dtype = numpy.int)
    
    ans[:mid, :mid] = s1 + s4 - s5 + s7
    ans[mid:, :mid] = s2 + s4
    ans[:mid, mid:] = s3 + s5
    ans[mid:, mid:] = s1 + s3 - s2 + s6
    
    return ans
    
      

if __name__ == "__main__":
    n = int(input())
    
    pow2 = 1 << (ceil(log2(n)))
    first = numpy.zeros( (pow2, pow2), dtype = numpy.int)
    second = numpy.zeros(( pow2, pow2), dtype = numpy.int)
    
    mat = numpy.loadtxt(sys.stdin, dtype = numpy.int, ndmin=2)
    
    first[:n,:n]=mat[:n]
    second[:n,:n]=mat[n:]
    
    ans = strassen(first, second)
    
    for l in ans[:n]:
        print(' '.join(map(str, l[:n])))

def verbing(s):
    l = len(s)
    if l >= 3:
        if (s[-3:] == 'ing'):
            s += 'ly'
        else:
            s += 'ing'
    return s


def not_bad(s):
    badpos = s.find('bad')
    notpos = s.find('not')
    if notpos < badpos and notpos != -1:
        s = s[:notpos] + 'good' + s[badpos+3:]    
    return s

def front_back(a, b):
    la = len(a)
    lb = len(b)

    return a[:(la+1)//2] + b[:(lb+1)//2] + a[(la+1)//2:] + b[(lb+1)//2:]

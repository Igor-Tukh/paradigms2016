def verbing(s):
	l = len(s)
	if (l >= 3):
		if (s[l-3:l:1] == 'ing'):
			s += 'ly'
		else:
			s += 'ing'
	return s


def not_bad(s):
	badpos = s.find('bad')
	notpos = s.find('not')
	if (notpos < badpos and notpos != -1):
		s = s[0:notpos:1] + 'good' + s[badpos+3:len(s):1]	
	return s

def front_back(a, b):
    la = len(a)
    lb = len(b)

    return a[0:(la+1)//2:1] + b[0:(lb+1)//2:1] + a[(la+1)//2:la:1] + b[(lb+1)//2:lb:1]

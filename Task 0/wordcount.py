import sys
 
def print_words(filename):
	total = get_words(filename)            # Using my own reading words from file that has been written earlier
	#total = your_reading(filename) # This function use your reading words from file
	total.sort()

	for a, b in total:
		print('{} {}'.format(a, b))

	#Output in text file - for more comfort
	#fo = open('output.txt', 'w')
	#for (a, b) in total:
	#	fo.write(a + ' ' + str(b) + '\n')

def print_top(filename):
	total = get_words(filename) #using my own reading words from file that has been written earlier 
	#total = your_reading(filename) # This function use your reading words from file
	total.sort(key=lambda x: x[1])
 
	for a, b in total[:-21:-1]:
		print('{} {}'.format(a, b))
   	
	#Output in text file - for more comfort
	#fo = open('output.txt', 'w')
	#for (a, b) in total:
	#	fo.write(a + ' ' + str(b) + '\n')
	
def get_words(filename):            # My own reading words from file
	f = open(filename, 'r')
	words = []
	for s in f.readlines():
		s = s.lower()
		cur1 = list(s.split())
		for s1 in cur1:
			s1.replace(',', '.')
			s1.replace('!', '.')
			s1.replace('?', '.')
			s1.replace(':', '.')
			cur2 = list(s1.split('.'))
			for word in cur2:
				if (len(word) > 0):
					words.append(word)
	dt = {}
	for word in words:
		if word in dt:
			dt[word] = dt[word] + 1
		else:
			dt[word] = 1
	return list(dt.items())

def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words
	
def your_reading(filename):  # This function use your words reading
	words = read_words(filename)
	dt = {}
	for word in words:
		if word in dt:
			dt[word] = dt[word] + 1
		else:
			dt[word] = 1
                      
	return list(dt.items())

def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)
 
    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)
 
if __name__ == '__main__':
    main()
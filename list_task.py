def remove_adjacent(lst):
    ans = []  
    if (len(lst) != 0):
    	last = a[0] - 1
    	for i in lst:
    		if (i != last):
    			last = i
    			ans.append(i)
    return ans

def linear_merge(lst1, lst2):
    i = 0
    j = 0
    ans = []
    l1 = len(lst1)
    l2 = len(lst2)

    for k in range(l1 + l2):
    	if (i >= l1 or (j < l2 and lst2[j] < lst1[i])):
    		ans.append(lst2[j])
    		j += 1
    	else:
    		ans.append(lst1[i])
    		i += 1
    return ans



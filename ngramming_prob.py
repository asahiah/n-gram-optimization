from collections import defaultdict
tuples_list = [(1, 2, 3), (1, 4, 3), (2, 5, 6), (1, 9, 3), (2, 8, 6), (3, 7, 9)]
tuples_count = [ 30, 20, 10, 5, 15, 25]

def group_tuples(tuples_list, tuples_count, n):
    groupedL, groupedM, groupedR = defaultdict(list), defaultdict(list), defaultdict(list)

    if n == 3:  # working with trigrams
        for t in tuples_list:
            keyL = (t[1], t[2])    # second and third elements as key
            groupedL[keyL].append(t)
            keyM = (t[0], t[2])  # First and third elements as key
            groupedM[keyM].append(t)
            keyR = (t[0], t[1])   # First and second elements as key
            groupedR[keyR].append(t)
        return [dict(groupedL), dict(groupedM), dict(groupedR)]  # Convert defaultdicts to regular dictionaries for display
    elif n == 2: # working with bigrams
        for t in tuples_list:
            keyL = t[1]   # second as key
            groupedL[keyL].append(t)
            keyR = t[0]   # First as key
            groupedR[keyR].append(t)
        return [dict(groupedL), dict(groupedR) ] # Convert defaultdicts to regular dictionaries for display

result = group_tuples(tuples_list, 3)
def genprobability(result, tuples_list, tuples_count):
    newtrigramdict = {}
    alltrigramsum = 0
    for key, val in result.items():
        trigramsum = 0
        for trigram in val:
            trigramsum = trigramsum + tuples_count[tuples_list.index(trigram)]
        probab = 0.0
        for trigram in val:
            probab = float(tuples_count[tuples_list.index(trigram)])/trigramsum
            newtrigramdict[trigram] = probab
        alltrigramsum = alltrigramsum + trigramsum
    for key, val in newtrigramdict.items():
        probability = (float(tuples_count[tuples_list.index(key)])/alltrigramsum) * val
        newtrigramdict[key] = probability
##    newsum = 0
    multiplier = 1.0/sum(iter(newtrigramdict.values())
##    for key, val in newtrigramdict.items():
##        newsum = newsum + newtrigramdict[key]
##        multiplier = 1.0/newsum
    for key, val  in newtrigramdict.items():
        newtrigramdict[key] = val*multiplier
    return (newtrigramdict)
    
    

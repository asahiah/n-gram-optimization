import networkx as nx
import matplotlib.pyplot as plt
from nltk.util import ngrams
from collections import Counter, defaultdict
import os, os.path

def extractpath(givenpath):
    directory, filename = os.path.split(givenpath)
    name, extension = os.path.splitext(filename)
    return directory, name, extension


def genprobability(tuples_list, tuples_count, n):
    results = group_tuples(tuples_list, n)
    super_outcome = []
    for result in results:
        newXgramdict = {}
        allXgramsum = 0
        for key, val in result.items():
            Xgramsum = 0
            for Xgram in val:
                Xgramsum = Xgramsum + tuples_count[tuples_list.index(Xgram)]
            probab = 0.0
            for Xgram in val:
                probab = float(tuples_count[tuples_list.index(Xgram)])/Xgramsum
                newXgramdict[Xgram] = probab
            allXgramsum = allXgramsum + Xgramsum
        for key, val in newXgramdict.items():
            probability = (float(tuples_count[tuples_list.index(key)])/allXgramsum) * val
            newXgramdict[key] = probability
        multiplier = 1.0/sum(iter(newXgramdict.values()))
        for key, val  in newXgramdict.items():
            newXgramdict[key] = val*multiplier
        super_outcome.append(newXgramdict)
    return super_outcome
                             

def group_tuples(tuples_list, n):
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

def my_ngram(file, n):
    #open input file and generate tokens to be used to build ngram
    with open(file, mode='r', encoding='utf8') as infile:
        text = infile.read().lower()
    # Tokenize words
    words = text.strip('\ufeff').strip().split()
    
    if n == 3:
        # Generate trigrams (3-grams)
        grams = list(ngrams(words, 3))
        # Count frequency of trigrams
    elif n == 2:
        # Generate bigrams (2-grams)
        grams = list(ngrams(words, 2))
        # Count frequency of bigrams
    gramm_counts = Counter(grams) # generate counts for each ngram
    listofkeys = list(gramm_counts.keys())
    listofvalues = list(gramm_counts.values())
    batch_outcome =  genprobability(listofkeys, listofvalues, n)   
    grammage = {2: ['BigL', 'BigR'], 3:['TrigL', 'TrigM', 'TrigR']}
    subnames = grammage[n]
    folder, filehead, filextension = extractpath(file)
    
    for igram in range(0, len(batch_outcome)):
        gram_name = subnames[igram]
        gramming = batch_outcome[igram]
        gram_counts = {k : v for k, v in sorted(gramming.items(), key=lambda item: item[0])}  # sort the counter and convert to dictionary
        outputfile = os.path.join(folder, filehead+'_'+ gram_name+filextension)  #prepare name of  output file    
        with open(outputfile,   mode= 'w',  encoding='utf8') as outfile:
            counting = 0
            for key,  value in gram_counts.items():
                #counting = counting + 1
                #if counting > 1000: break
                outfile.write(str(key)+" "+ str(value)+'\n')
        print(f"File number {igram+1} out of {len(batch_outcome)} printed with name {outputfile}.")


if __name__ == '__main__':
    file = input("Supply file name or file path: ")
    gram_size = int(input("Supply size of ngram, 2 or 3: "))
    my_ngram(file, gram_size)
    

from scipy.special import comb
import numpy as np
from collections import Counter
import math

class Pokertest:
    def pokerTest(s,m):
        X2theoretical = [3.84,5.99,7.81,9.48,11.07,12.59,14.06]
        k = len(s)//m
        l = list(np.arange(0,k))
        s1 = s
        for i in range(0,k):
            while len(s1) > 0:
                l[i] = s1[:m]
                s1 = s1[m:]
                break
        n = l
        for j,i in enumerate(l):
            try:
                n[j] = Counter(i)['1']
            except:
                n[j] = Counter(i)['0']
            
        n.sort()
        niDict = dict(Counter(n))
        #we create a dummy dictionary with keys 
        k =[i for i in range(0,m+1)]
        dummydict = dict(zip(k,[0]*len(k)))
        def check_existance(i,collection: iter):
            return i in collection
        if dummydict.keys() == niDict.keys():
            print('ok')
        else:
            for i in dummydict.keys():
                if check_existance(i,niDict.keys()) == False:
                    niDict[i] = 0
        b = []

        for i in niDict.keys():
        
            numerator = math.pow(niDict[i] - comb(m,i)*len(s)/((2**m)*m),2)
            denominator = comb(m,i)*len(s)/((2**m)*m)
            S = numerator / denominator
            b.append(S)
            
        X2 = sum(b)
        if X2 < X2theoretical[m-1]:
            return True
            #print('The sequence is random')
        else:
            return False
            #print('The sequence is not random')
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk 
from nltk.corpus import brown
import collections


# In[ ]:


# frequency function 
def fre(x):
    from collections import Counter
    types =  Counter(tuple(x) for x in x )
    #print(types)

    # storing it as a list 
    freq = []
    for value in types.items() :
        freq.append(value)

    #sorting the list in decending order
    def sortthird(freq): 
        return freq[1] 
    freq.sort(key = sortthird ,reverse = True) 
    #print(freq)
    return freq


# In[ ]:


# insert start "<s>" and end "<\s>" symbols for each sentence 
p = brown.tagged_sents()
brown_corpus = []
for i in p :
    i.insert(0,('<s>','<s>'))
    i.insert(len(i),('<\s>','<\s>'))
    brown_corpus.append(i)


# In[ ]:


# creating test and training sets from the brown corpus
# test set contains first 100 sentences
brown_test = []
brown_train = []
sen = 0
for i in brown_corpus:
    sen += 1
    if sen <= 10:
        brown_test.append(i)
    else:
        brown_train.append(i)


# In[ ]:


#converting training set to a [word,tag] sequence
brown_words_tag = []
for i in brown_train:
    for j in i:
        brown_words_tag.append(j)


# In[ ]:


# frequency of each [word,tag] 
fre_wordtag = fre(brown_words_tag)
#print(fre_wordtag)

#frerquency of ti (just the tags) 
brown_tag = []
for i in brown_train:
    for j in i:
         brown_tag.append(j[1])

# getting frequencies of each tag in brown_tag
types =  collections.Counter(brown_tag)
fre_tag = []
for value in types.items() :
    fre_tag.append(value)
    
#sorting the list in decending order
def sortthird(fre_tag): 
    return fre_tag[1] 
fre_tag.sort(key = sortthird ,reverse = True)


# In[ ]:


# probabitity of p(wi|ti)
probWiti = []
list1 =[]
list2 = []
list3 = []
for i in fre_wordtag:
    for j in fre_tag:
        if i[0][1] == j[0]:
            temp = [i[0] , i[1]/j[1]]
            probWiti.append(temp)
            list1.append(i[0][0])
            temp1 = [i[0][1], i[1]/j[1]]
            list2.append(temp1)
            
            
            

#probability of p{ti|t(i-1)}


#frequency of [ti,t(i-1)]             #Step 1
bi_tag = []
x = len(brown_words_tag)
for j in range(x):
    if j+1 < x:  
        temp = [brown_words_tag[j][1] , brown_words_tag[j+1][1]]
        if temp != ['<\s>' ,'<s>' ]:
            bi_tag.append(temp)

fre_bi_tag= fre(bi_tag)   #Step 2

# probabitity
probbitag = []             #Step 3
for i in fre_bi_tag:
    for j in fre_tag:
        if i[0][0] == j[0]:
            temp = [i[0] , i[1]/j[1]]
            probbitag.append(temp)          

pos_tag = [] 
for i in fre_tag:
    pos_tag.append(i[0])


# In[ ]:


# vitervi algorithm

# creating lattice of transition and emissions probability

#emission probability for a sentence
l = len(sentence)
c = 1
sentence = brown_test[4]    # change the sentence by replacing [i] to try out different sentences from brown_test; i={0,10}
lattic_emission = [[] for i in range(l)]  # emission probability lattice
sen_tag = []                              # set of all different tags the sentence could have
for i in range(l):
    for j in probWiti:
        if sentence[i][0] == j[0][0]: 
            lattic_emission[i].append(j) # lattice will only have element whose emission probability > 0, since for 0 emission probability, the final probability becomes zero
            if j[0][1] not in sen_tag:
                sen_tag.append(j[0][1]) # set of all posible tags the sentence could have
    if(len(lattic_emission[i])== 0):    # for unknown words in sentence 
        temp = [(sentence[i][0], 'NN') , 0.11 ] # 'unk' tags are assumed to be 'NN' since they are the most occuring tags with a 11% probability 
        lattic_emission[i].append(temp)
                
       
            
#transition tags for this sentence
l = len(sen_tag) 
tran_tag = []
for i in sen_tag:
    for j in sen_tag:
        temp = (i , j)
        if temp not in tran_tag: # avoid repetitions 
            tran_tag.append(temp)
            

            
#transition probability for this sentence
tran_pro = []
for i in tran_tag:
    for j in probbitag:
        if i == j[0]:  
            tran_pro.append(j) # the tag pairs not in probbitag have zero probability. Again, we are not considering them since result for such sentence will have 0 probability
mat = []
for i in lattic_emission:
    temp = [i[0][0][0], len(i)]
    mat.append(temp)       

max_emission = []
sequence = []
for i in lattic_emission:
    def sortthird(i): 
        return i[1] 
    i.sort(key = sortthird ,reverse = True) # getting maximum emission probability after each step
    max_emission.append(i)
l = len(mat)
vi = []
for i in range(l-1):
    if i < l:
        temp =(max_emission[i][0][0][1],max_emission[i+1][0][0][1])
        vi.append(temp)
        sequence.append(max_emission[i][0][0])
temp = ('<\s>', '<\s>')
sequence.append(temp)
l = len(vi)
Vj = [] #argmax from multiplication of transition and emission probabilities 
m = 0
for i in range(l):
    for j in tran_pro:
        m += 1
        if vi[i] == j[0]:
            temp = max_emission[i][0][1]*j[1]
            Vj.append(temp)
            temp1= [max_emission[i][0][0],j[0]]
    temp1= [max_emission[i][0][0],j[0]]
    if(temp1 not in sequence):
        temp1= [max_emission[i][0][0],j[0]]
        
def viterbi(Vj) : 
    result = 1
    for x in Vj: 
         result = result * x  
    return result         
Viterbi = viterbi(Vj)
print(sequence , '\n' ,Viterbi)


# In[ ]:


# Accuracy 
l = len(sentence)
count = 0
for i in range(l):
    if sentence[i] == sequence[i]:
        count +=1
accuracy = (count / len(sentence))*100
print("accuracy of HMM tagger for given sentence is ")
print(accuracy)


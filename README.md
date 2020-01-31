A frankensteined  HMM POS tagger


This HMM addresses the problem of part-of-speech tagging. It estimates
the probability of a tag sequence for a given word sequence as follows:
Say words = w1....wN
and tags = t1..tN
then,
P(tags | words) is_proportional_to  product P(ti | t{i-1}) P(wi | ti)
To find the best tag sequence for a given sequence of words, we want to find the tag sequence that has the maximum P(tags | words)


Example: 
P("I want to run") = P(START) * P(PP|START) * P(I | PP) * P(VB | PP) * P(want | VB) * P(TO | VB) * P(to | TO) * 
P(VB | TO) * P(run | VB) * P(END | VB)

i.e ( P(w/t)* P(ti/ti-1))

Now an obvious question pops up.
The words in the sentence may have many tags which leads to different probabilities for the same sentence, each corresponding to a different combination of possible tags. 
We need to find the combination which produces the highest probability for the sentence - Virtebi algorithm provides a quick way to do so.

## viterbi:
for each step i in 1 .. sentlen,
store a dictionary
that maps each tag X
to the probability of the best tag sequence of length i that ends in X

backpointer:
for each step i in 1..sentlen,
store a dictionary
that maps each tag X
to the previous tag in the best tag sequence of length i that ends in X

 if the tag is X and the current word is w, then
 find the previous tag Y such that
 the best tag sequence that ends in X
 actually ends in Y X
 that is, the Y that maximizes
 prev_viterbi[Y] * P(X | Y) * P( w | X)

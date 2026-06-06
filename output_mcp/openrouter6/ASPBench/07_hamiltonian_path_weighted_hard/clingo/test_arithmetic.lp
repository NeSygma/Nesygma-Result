vertex(0..2).
edge(i, j) :- vertex(i), vertex(j), j = i+1.
#show edge/2.
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7).

edge(1,2). edge(1,3). edge(2,3). edge(2,4). edge(3,5). edge(4,6). edge(5,6). edge(5,7). edge(6,7).

{dominating_set(V) : vertex(V)}.

covered(V) :- dominating_set(V).
covered(V) :- edge(V,N), dominating_set(N).

:- not covered(1).
:- not covered(2).
:- not covered(3).
:- not covered(4).
:- not covered(5).
:- not covered(6).
:- not covered(7).

#minimize { V : dominating_set(V) }.

size(N) :- #count{ V : dominating_set(V) } = N.

#show dominating_set/1.
#show size/1.
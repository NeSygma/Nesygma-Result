% Fragments
fragment(0). fragment(1). fragment(2). fragment(3). fragment(4). fragment(5). fragment(6). fragment(7).

% Positions 0..7
pos(0..7).

% Overlap facts (directed) with length >=3
overlap(0,1,6).
overlap(0,2,4).
overlap(1,2,6).
overlap(1,3,4).
overlap(2,3,6).
overlap(2,4,4).
overlap(3,4,6).
overlap(3,5,4).
overlap(4,5,6).
overlap(4,6,4).
overlap(5,6,6).
overlap(5,7,4).
overlap(6,7,6).
overlap(7,0,3).
overlap(7,2,3).

% Permutation: each fragment assigned to exactly one position
1 { at(F,P) : pos(P) } 1 :- fragment(F).
1 { at(F,P) : fragment(F) } 1 :- pos(P).

% Adjacent overlap constraint
:- at(F1,P), at(F2,P1), P1 = P+1, not overlap(F1,F2,_).

% Compute total overlap sum
total(S) :- S = #sum { L,P : at(F1,P), at(F2,P1), P1 = P+1, overlap(F1,F2,L) }.

#show at/2.
#show total/1.
#minimize { -L, P : at(F1,P), at(F2,P1), P1 = P+1, overlap(F1,F2,L) }.
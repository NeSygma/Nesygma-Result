%%% Bin Packing Problem
%%% 9 items, bin capacity 10, minimize bins used

%%% Domain Definitions
item(1..9).
bin(1..9).  % Upper bound: at most 9 bins (worst case: one item per bin)
capacity(10).

%%% Item sizes
size(1,4).
size(2,6).
size(3,2).
size(4,3).
size(5,7).
size(6,1).
size(7,5).
size(8,2).
size(9,4).

%%% 1. Each item assigned to exactly one bin
1 { assign(I, B) : bin(B) } 1 :- item(I).

%%% 2. No bin exceeds capacity
:- bin(B), capacity(C), #sum { S, I : assign(I,B), size(I,S) } > C.

%%% 3. Minimize number of bins used
used(B) :- assign(_, B).
#minimize { 1, B : used(B) }.

%%% Show results
#show assign/2.
#show used/1.
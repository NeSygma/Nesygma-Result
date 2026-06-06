%% Facts: items and sizes
item(1..9).
size(1,4). size(2,6). size(3,2). size(4,3). size(5,7). size(6,1). size(7,5). size(8,2). size(9,4).

%% Bin capacity
capacity(10).

%% Maximum possible bins (upper bound)
max_bins(9).
bin(1..M) :- max_bins(M).

%% Each item assigned to exactly one bin
{ assign(I,B) : bin(B) } 1 :- item(I).

%% A bin is used if at least one item is assigned to it
used(B) :- assign(_, B).

%% Capacity constraint: total size per bin must not exceed capacity
:- bin(B), capacity(C), #sum { S, I : assign(I,B), size(I,S) } > C.

%% Minimize the number of bins used
#minimize { 1, B : used(B) }.

%% Output
#show assign/2.
#show used/1.
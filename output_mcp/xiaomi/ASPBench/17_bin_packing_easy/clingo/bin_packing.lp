% Bin Packing Problem - Minimize number of bins

% ============ DATA ============
% Items and their sizes
item(1..9).
size(1, 4).
size(2, 6).
size(3, 2).
size(4, 3).
size(5, 7).
size(6, 1).
size(7, 5).
size(8, 2).
size(9, 4).

% Bin capacity
capacity(10).

% Maximum number of bins (upper bound - at most 9 bins needed)
max_bins(9).
bin(1..9) :- max_bins(N), N >= 1.

% ============ DECISION VARIABLES ============
% Each item assigned to exactly one bin
1 { assign(I, B) : bin(B) } 1 :- item(I).

% ============ DERIVED PREDICATES ============
% A bin is used if at least one item is assigned to it
bin_used(B) :- assign(I, B).

% Calculate total size in each bin
bin_total(B, T) :- bin(B), T = #sum { S, I : assign(I, B), size(I, S) }.

% Count number of bins used
num_bins(N) :- N = #count { B : bin_used(B) }.

% ============ CONSTRAINTS ============
% No bin can exceed capacity
:- bin_total(B, T), capacity(C), T > C.

% ============ OBJECTIVE ============
% Minimize the number of bins used
#minimize { 1, B : bin_used(B) }.

% ============ OUTPUT ============
#show assign/2.
#show bin_used/1.
#show bin_total/2.
#show num_bins/1.
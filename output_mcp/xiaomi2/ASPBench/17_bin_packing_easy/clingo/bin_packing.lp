% Bin Packing Problem
% Minimize number of bins used while respecting capacity constraints

% Items and their sizes
item(1). item(2). item(3). item(4). item(5). item(6). item(7). item(8). item(9).

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

% Bin domain - at most as many bins as items
bin(1..9).

% Assign each item to exactly one bin
1 { assign(I, B) : bin(B) } 1 :- item(I).

% Calculate total size in each bin
bin_size(B, S) :- bin(B), S = #sum { Sz, I : assign(I, B), size(I, Sz) }.

% Capacity constraint - no bin can exceed capacity
:- bin_size(B, S), capacity(C), S > C.

% A bin is used if at least one item is assigned to it
used(B) :- assign(I, B).

% Count the number of bins used
num_bins(N) :- N = #count { B : used(B) }.

% Minimize the number of bins used
#minimize { 1, B : used(B) }.

% Output formatting
#show assign/2.
#show num_bins/1.
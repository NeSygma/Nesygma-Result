% Bin Packing Problem
% Items and their sizes
item(1..9).
size(1,4). size(2,6). size(3,2). size(4,3). size(5,7). 
size(6,1). size(7,5). size(8,2). size(9,4).

% Bin capacity
capacity(10).

% We can use up to 9 bins (one per item)
bin(1..9).

% Each item assigned to exactly one bin
1 { assign(Item, Bin) : bin(Bin) } 1 :- item(Item).

% Compute total size per bin using aggregate
total_size(Bin, S) :- bin(Bin), S = #sum { Size, Item : assign(Item, Bin), size(Item, Size) }.

% Bin capacity constraint
:- bin(Bin), total_size(Bin, S), S > 10.

% Define which bins are used (have at least one item)
used(Bin) :- assign(_, Bin).

% Count number of bins used
num_bins(N) :- N = #count { Bin : used(Bin) }.

% Minimize number of bins used
#minimize { 1, Bin : used(Bin) }.

% Feasibility: solution exists if all items assigned and capacity respected
feasible :- item(Item), assign(Item, _), not (bin(Bin), total_size(Bin, S), S > 10).

% Show relevant information
#show assign/2.
#show used/1.
#show total_size/2.
#show num_bins/1.
#show feasible/0.
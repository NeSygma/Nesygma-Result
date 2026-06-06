% Define items and their sizes
item(1). size(1,4).
item(2). size(2,6).
item(3). size(3,2).
item(4). size(4,3).
item(5). size(5,7).
item(6). size(6,1).
item(7). size(7,5).
item(8). size(8,2).
item(9). size(9,4).

% Bin capacity
bin_capacity(10).

% Choice rule: create bins as needed (up to a reasonable limit)
{ bin(Bin) : Bin = 1..10 }.

% Choice rule: assign each item to exactly one bin
{ assigned(Item, Bin) : bin(Bin) } = 1 :- item(Item).

% Define which bins are used
used_bin(Bin) :- assigned(_, Bin).

% Constraint: bin capacity must not be exceeded
:- bin(Bin), bin_capacity(C), #sum { Size, I : size(I, Size), assigned(I, Bin) } > C.

% Objective: minimize the number of bins used
#minimize { 1@1, Bin : used_bin(Bin) }.

% Show the solution
#show assigned/2.
#show used_bin/1.
#show feasible.
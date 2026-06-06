% Items (27 total)
item(1, 9, electronics, fragile, high).
item(2, 8, electronics, sturdy, high).
item(3, 3, electronics, sturdy, high).
item(4, 9, liquid, fragile, high).
item(5, 7, liquid, sturdy, high).
item(6, 4, liquid, sturdy, high).
item(7, 10, electronics, fragile, high).
item(8, 10, standard, sturdy, high).
item(9, 10, liquid, fragile, high).
item(10, 10, standard, sturdy, high).
item(11, 8, standard, sturdy, high).
item(12, 7, standard, sturdy, high).
item(13, 5, standard, sturdy, low).
item(14, 8, standard, fragile, low).
item(15, 6, standard, fragile, low).
item(16, 6, standard, sturdy, low).
item(17, 8, standard, fragile, low).
item(18, 6, standard, fragile, low).
item(19, 6, standard, sturdy, low).
item(20, 7, standard, sturdy, low).
item(21, 7, standard, sturdy, low).
item(22, 6, standard, sturdy, low).
item(23, 7, standard, sturdy, low).
item(24, 5, standard, fragile, low).
item(25, 5, standard, fragile, low).
item(26, 3, standard, sturdy, low).
item(27, 5, standard, sturdy, low).

% Bin capacity
bin_capacity(20).

% Bin IDs 1-6 must exist (for priority items)
bin(1..6).

% Additional bins can be created as needed (up to 20 total)
{ bin(B) : B = 7..20 }.

% Helper predicates
category(Item, Cat) :- item(Item, _, Cat, _, _).
fragile(Item) :- item(Item, _, _, fragile, _).
high_priority(Item) :- item(Item, _, _, _, high).
low_priority(Item) :- item(Item, _, _, _, low).

% Assignment: each item to exactly one bin
1 { assigned(Item, Bin) : bin(Bin) } 1 :- item(Item).

% Capacity constraint: total size in bin <= 20
:- assigned(Item, Bin), bin_capacity(Cap),
   #sum { Size : assigned(I, Bin), item(I, Size, _, _, _) } > Cap.

% Incompatibility: electronics and liquids cannot be in same bin
:- assigned(Item1, Bin), assigned(Item2, Bin), Item1 < Item2,
   category(Item1, electronics), category(Item2, liquid).
:- assigned(Item1, Bin), assigned(Item2, Bin), Item1 < Item2,
   category(Item1, liquid), category(Item2, electronics).

% Fragility limit: no more than 2 fragile items per bin
:- assigned(Item, Bin), fragile(Item),
   #count { I : assigned(I, Bin), fragile(I) } > 2.

% Priority placement: high-priority items only in bins 1-6
:- assigned(Item, Bin), high_priority(Item), Bin > 6.

% Show the assignment
#show assigned/2.
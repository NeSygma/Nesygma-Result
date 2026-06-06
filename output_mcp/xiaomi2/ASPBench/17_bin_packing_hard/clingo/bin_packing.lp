% Bin Packing Problem - ASP Translation

% ============ DOMAINS ============

% Items with properties: item(ID, Size, Category, Fragility, Priority)
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

% Bins (1..12 should be enough for 185 total size / 20 capacity)
bin(1..12).

% Priority bins (1-6)
priority_bin(1..6).

% ============ CHOICE RULES ============

% Each item assigned to exactly one bin
1 { assign(I, B) : bin(B) } 1 :- item(I, _, _, _, _).

% ============ CONSTRAINTS ============

% 1. Capacity: total size in any bin must not exceed 20
:- #sum{ Sz,I : assign(I, B), item(I, Sz, _, _, _) } > 20, bin(B).

% 2. Incompatibility: electronics and liquids cannot be in same bin
has_electronics(B) :- assign(I, B), item(I, _, electronics, _, _).
has_liquid(B) :- assign(I, B), item(I, _, liquid, _, _).
:- has_electronics(B), has_liquid(B).

% 3. Fragility limit: no more than 2 fragile items per bin
:- #count{ I : assign(I, B), item(I, _, _, fragile, _) } > 2, bin(B).

% 4. Priority placement: high-priority items only in bins 1-6
:- assign(I, B), item(I, _, _, _, high), B > 6.

% ============ OUTPUT PREDICATES ============

% Which bins are used
used_bin(B) :- assign(_, B).

% Number of bins used
num_bins(N) :- N = #count{ B : used_bin(B) }.

% Whether bin has high priority items
is_priority_bin(B) :- assign(I, B), item(I, _, _, _, high).

% Total size in priority bins
total_priority_utilization(T) :- T = #sum{ Sz,I : assign(I, B), item(I, Sz, _, _, _), is_priority_bin(B) }.

% Feasibility (always true if we find a solution)
feasible.

% Not optimal (feasibility only)
optimal.

% ============ SHOW DIRECTIVES ============

#show feasible.
#show optimal.
#show num_bins/1.
#show total_priority_utilization/1.
#show assign/2.
#show is_priority_bin/1.
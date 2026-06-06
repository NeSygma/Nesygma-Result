% --- Data ---
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

bin(1..27).

% --- Assignment ---
1 { assigned(I, B) : bin(B) } 1 :- item(I, _, _, _, _).

% --- Constraints ---
% 1. Capacity: Max 20
:- bin(B), #sum { S, I : assigned(I, B), item(I, S, _, _, _) } > 20.

% 2. Fragility Limit: Max 2 fragile items
:- bin(B), #count { I : assigned(I, B), item(I, _, _, fragile, _) } > 2.

% 3. Incompatibility: Electronics and liquids cannot be in the same bin
has_electronics(B) :- assigned(I, B), item(I, _, electronics, _, _).
has_liquid(B) :- assigned(I, B), item(I, _, liquid, _, _).
:- bin(B), has_electronics(B), has_liquid(B).

% 4. Priority Placement: High-priority only in bins 1-6
:- assigned(I, B), item(I, _, _, _, high), B > 6.

% --- Output Helpers ---
is_priority_bin(B) :- assigned(I, B), item(I, _, _, _, high).
bin_used(B) :- assigned(I, B).

#show assigned/2.
#show bin_used/1.
#show is_priority_bin/1.
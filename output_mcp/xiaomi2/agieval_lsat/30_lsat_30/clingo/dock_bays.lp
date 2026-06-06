% Domain: bays 1-6
bay(1..6).

% Cargo types
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay holds exactly one cargo type
1 { assign(B, C) : cargo(C) } 1 :- bay(B).

% Each cargo type is in exactly one bay
1 { assign(B, C) : bay(B) } 1 :- cargo(C).

% Helper: get bay number for a cargo
bay_of(C, B) :- assign(B, C).

% Constraint 1: grain > livestock (higher bay number)
:- bay_of(grain, BG), bay_of(livestock, BL), BG <= BL.

% Constraint 2: livestock > textiles
:- bay_of(livestock, BL), bay_of(textiles, BT), BL <= BT.

% Constraint 3: produce > fuel
:- bay_of(produce, BP), bay_of(fuel, BF), BP <= BF.

% Constraint 4: textiles is next to produce (adjacent)
:- bay_of(textiles, BT), bay_of(produce, BP), |BT - BP| != 1.

% Evaluate each answer choice for bays 1-3
% A: fuel, machinery, textiles
a_correct :- assign(1, fuel), assign(2, machinery), assign(3, textiles).
% B: grain, machinery, fuel
b_correct :- assign(1, grain), assign(2, machinery), assign(3, fuel).
% C: machinery, livestock, fuel
c_correct :- assign(1, machinery), assign(2, livestock), assign(3, fuel).
% D: machinery, textiles, fuel
d_correct :- assign(1, machinery), assign(2, textiles), assign(3, fuel).
% E: machinery, textiles, produce
e_correct :- assign(1, machinery), assign(2, textiles), assign(3, produce).

option(a) :- a_correct.
option(b) :- b_correct.
option(c) :- c_correct.
option(d) :- d_correct.
option(e) :- e_correct.

#show option/1.
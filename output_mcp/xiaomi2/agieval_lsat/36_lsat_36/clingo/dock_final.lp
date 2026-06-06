% Domains
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay gets exactly one cargo
{ assign(B, C) : cargo(C) } 1 :- bay(B).

% Each cargo is assigned to exactly one bay
1 { assign(B, C) : bay(B) } 1 :- cargo(C).

% Bay 4 holds produce
assign(4, produce).

% Constraint 1: grain > livestock
:- assign(B1, grain), assign(B2, livestock), B1 <= B2.

% Constraint 2: livestock > textiles
:- assign(B1, livestock), assign(B2, textiles), B1 <= B2.

% Constraint 3: produce > fuel
:- assign(B1, produce), assign(B2, fuel), B1 <= B2.

% Adjacency
adjacent(B1, B2) :- bay(B1), bay(B2), |B1 - B2| = 1.

% Constraint 4: textiles next to produce
:- assign(B1, textiles), assign(B2, produce), not adjacent(B1, B2).

% Count determined bays (bays with same cargo in all models)
% We use a two-scenario approach to find max differing bays
scenario(1..2).
{ sassign(S, B, C) : cargo(C) } 1 :- bay(B), scenario(S).
1 { sassign(S, B, C) : bay(B) } 1 :- cargo(C), scenario(S).
sassign(S, 4, produce) :- scenario(S).
:- sassign(S, B1, grain), sassign(S, B2, livestock), B1 <= B2.
:- sassign(S, B1, livestock), sassign(S, B2, textiles), B1 <= B2.
:- sassign(S, B1, produce), sassign(S, B2, fuel), B1 <= B2.
:- sassign(S, B1, textiles), sassign(S, B2, produce), not adjacent(B1, B2).

differ(B) :- bay(B), sassign(1, B, C1), sassign(2, B, C2), C1 != C2.
#maximize { 1, B : differ(B) }.

diff_count(N) :- N = #count { B : differ(B) }.

% 4 bays determined means 2 can differ
option(a) :- diff_count(4).
option(b) :- diff_count(3).
option(c) :- diff_count(2).
option(d) :- diff_count(1).
option(e) :- diff_count(0).

#show option/1.
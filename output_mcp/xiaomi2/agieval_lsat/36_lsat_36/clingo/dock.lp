% Domains
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).
scenario(1..2).

% Each bay gets exactly one cargo per scenario
{ assign(S, B, C) : cargo(C) } 1 :- bay(B), scenario(S).

% Each cargo is assigned to exactly one bay per scenario
1 { assign(S, B, C) : bay(B) } 1 :- cargo(C), scenario(S).

% Constraints (applied to each scenario)
:- assign(S, B1, grain), assign(S, B2, livestock), B1 <= B2.
:- assign(S, B1, livestock), assign(S, B2, textiles), B1 <= B2.
:- assign(S, B1, produce), assign(S, B2, fuel), B1 <= B2.

% Adjacency definition
adjacent(B1, B2) :- bay(B1), bay(B2), B1 = B2+1.
adjacent(B1, B2) :- bay(B1), bay(B2), B1 = B2-1.

% Textiles next to produce
:- assign(S, B1, textiles), assign(S, B2, produce), not adjacent(B1, B2).

% Condition: bay 4 holds produce in both scenarios
assign(S, 4, produce) :- scenario(S).

% Differ predicate: true if the two scenarios assign different cargo to a bay
differ(B) :- bay(B), assign(1, B, C1), assign(2, B, C2), C1 != C2.

% Maximize the number of bays where the two scenarios differ
#maximize { 1, B : differ(B) }.

% Count differing bays
diff_count(N) :- N = #count { B : differ(B) }.

% Map to answer choices
option(a) :- diff_count(4).
option(b) :- diff_count(3).
option(c) :- diff_count(2).
option(d) :- diff_count(1).
option(e) :- diff_count(0).

#show option/1.
#show diff_count/1.
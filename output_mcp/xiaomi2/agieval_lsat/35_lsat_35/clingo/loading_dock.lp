% Domains
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay holds exactly one cargo, each cargo in exactly one bay
1 { holds(B, C) : cargo(C) } 1 :- bay(B).
1 { holds(B, C) : bay(B) } 1 :- cargo(C).

% Constraint 1: grain > livestock
:- holds(B1, grain), holds(B2, livestock), B1 <= B2.

% Constraint 2: livestock > textiles
:- holds(B1, livestock), holds(B2, textiles), B1 <= B2.

% Constraint 3: produce > fuel
:- holds(B1, produce), holds(B2, fuel), B1 <= B2.

% Constraint 4: textiles is next to produce
:- holds(B1, textiles), holds(B2, produce), |B1 - B2| != 1.

% Constraint 5 (additional for question): produce is next to livestock
:- holds(B1, produce), holds(B2, livestock), |B1 - B2| != 1.

% Check each option
% A: Bay 2 is holding fuel
a_possible :- holds(2, fuel).
% B: Bay 4 is holding produce
b_possible :- holds(4, produce).
% C: Bay 4 is holding textiles
c_possible :- holds(4, textiles).
% D: Bay 5 is holding grain
d_possible :- holds(5, grain).
% E: Bay 5 is holding machinery
e_possible :- holds(5, machinery).

% The answer is the one that CANNOT be true
option(a) :- not a_possible.
option(b) :- not b_possible.
option(c) :- not c_possible.
option(d) :- not d_possible.
option(e) :- not e_possible.

#show option/1.
#show holds/2.
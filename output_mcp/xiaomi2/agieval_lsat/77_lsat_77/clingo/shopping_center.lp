% Domains
space(1..7).
business(opt; pharm; rest1; rest2; shoe; toy; vet).

% Each business assigned to exactly one space
1 { assign(B, S) : space(S) } 1 :- business(B).

% Each space has exactly one business
1 { assign(B, S) : business(B) } 1 :- space(S).

% Given: shoe store in space 2
assign(shoe, 2).

% Constraint 1: Pharmacy at one end, a restaurant at the other
end(1). end(7).
:- assign(pharm, S), not end(S).

% Helper: is there a restaurant at space S?
has_restaurant(S) :- assign(rest1, S).
has_restaurant(S) :- assign(rest2, S).

% If pharmacy at 1, restaurant must be at 7
:- assign(pharm, 1), not has_restaurant(7).
% If pharmacy at 7, restaurant must be at 1
:- assign(pharm, 7), not has_restaurant(1).

% Constraint 2: Two restaurants separated by at least two other businesses
:- assign(rest1, S1), assign(rest2, S2), S1 < S2, S2 - S1 < 3.
:- assign(rest1, S1), assign(rest2, S2), S2 < S1, S1 - S2 < 3.

% Constraint 3: Pharmacy next to optometrist or veterinarian
neighbor(S, S-1) :- space(S), S > 1.
neighbor(S, S+1) :- space(S), S < 7.
has_opt_or_vet_neighbor(S) :- assign(opt, N), neighbor(S, N).
has_opt_or_vet_neighbor(S) :- assign(vet, N), neighbor(S, N).
:- assign(pharm, S), not has_opt_or_vet_neighbor(S).

% Constraint 4: Toy store not next to veterinarian
:- assign(toy, S1), assign(vet, S2), neighbor(S1, S2).

% Choice over which option could be true
{ choose(1..5) } 1.

% Enforce that the chosen option is true in the assignment
:- choose(1), not assign(opt, 5).
:- choose(2), not assign(pharm, 1).
:- choose(3), not has_restaurant(3).
:- choose(4), not assign(toy, 6).
:- choose(5), not assign(vet, 4).

% Map chosen option to output
option(a) :- choose(1).
option(b) :- choose(2).
option(c) :- choose(3).
option(d) :- choose(4).
option(e) :- choose(5).

#show option/1.
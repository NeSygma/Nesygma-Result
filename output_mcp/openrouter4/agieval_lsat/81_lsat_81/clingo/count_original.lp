% Shopping center with 7 spaces, 7 businesses
space(1..7).

business(optometrist; pharmacy; restaurant1; restaurant2; shoe_store; toy_store; veterinarian).

% Each business in exactly one space, each space has exactly one business
1 { pos(B, S) : space(S) } 1 :- business(B).
1 { pos(B, S) : business(B) } 1 :- space(S).

% Symmetry breaking: restaurant1 before restaurant2
:- pos(restaurant1, S1), pos(restaurant2, S2), S1 >= S2.

% Adjacency relation
adjacent(S1, S2) :- space(S1), space(S2), S1 = S2 - 1.
adjacent(S1, S2) :- space(S1), space(S2), S2 = S1 - 1.

% Constraint 1: Pharmacy at one end, one restaurant at the other
:- not pos(pharmacy, 1), not pos(pharmacy, 7).
:- pos(pharmacy, 1), not pos(restaurant1, 7), not pos(restaurant2, 7).
:- pos(pharmacy, 7), not pos(restaurant1, 1), not pos(restaurant2, 1).

% Constraint 2: Two restaurants separated by at least two other businesses
:- pos(restaurant1, S1), pos(restaurant2, S2), |S1 - S2| <= 2.

% Constraint 3: Pharmacy next to optometrist or veterinarian
has_adj_opt_or_vet :- pos(pharmacy, S), pos(optometrist, S1), adjacent(S, S1).
has_adj_opt_or_vet :- pos(pharmacy, S), pos(veterinarian, S1), adjacent(S, S1).
:- not has_adj_opt_or_vet.

% Constraint 4: Toy store not next to veterinarian
:- pos(toy_store, S1), pos(veterinarian, S2), adjacent(S1, S2).

% Count solutions
#show pos/2.
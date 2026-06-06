% Domain: spaces
space(1..7).

% Domain: businesses
business(optometrist).
business(pharmacy).
business(restaurant1).
business(restaurant2).
business(shoe_store).
business(toy_store).
business(veterinarian).

% End spaces
end_space(1).
end_space(7).

% Adjacency relation
next_to(S1, S2) :- space(S1), space(S2), |S1 - S2| = 1.

% Each business assigned to exactly one space
1 { assigned(B, S) : space(S) } 1 :- business(B).

% Each space has exactly one business
1 { assigned(B, S) : business(B) } 1 :- space(S).

% Given: veterinarian is in space 5
assigned(veterinarian, 5).

% Constraint 1: Pharmacy at one end, one restaurant at the other end
assigned(pharmacy, S) :- end_space(S).
assigned(restaurant1, S) :- end_space(S), assigned(pharmacy, S2), S != S2.
assigned(restaurant2, S) :- end_space(S), assigned(pharmacy, S2), S != S2.

% Constraint 2: Two restaurants must be separated by at least 2 other businesses
:- assigned(restaurant1, S1), assigned(restaurant2, S2), |S1 - S2| < 3.

% Constraint 3: Pharmacy must be next to optometrist OR veterinarian
:- assigned(pharmacy, P), not next_to_opt_or_vet(P).
next_to_opt_or_vet(P) :- assigned(pharmacy, P), assigned(optometrist, O), next_to(P, O).
next_to_opt_or_vet(P) :- assigned(pharmacy, P), assigned(veterinarian, V), next_to(P, V).

% Constraint 4: Toy store cannot be next to veterinarian
:- assigned(toy_store, T), assigned(veterinarian, V), next_to(T, V).

% Evaluate answer choices
% A: Optometrist is in space 2
opt_a :- assigned(optometrist, 2).

% B: Pharmacy is in space 7
opt_b :- assigned(pharmacy, 7).

% C: A restaurant is in space 4
opt_c :- assigned(restaurant1, 4).
opt_c :- assigned(restaurant2, 4).

% D: Shoe store is in space 6
opt_d :- assigned(shoe_store, 6).

% E: Toy store is in space 3
opt_e :- assigned(toy_store, 3).

% Map to options
option(a) :- opt_a.
option(b) :- opt_b.
option(c) :- opt_c.
option(d) :- opt_d.
option(e) :- opt_e.

#show option/1.
#show assigned/2.
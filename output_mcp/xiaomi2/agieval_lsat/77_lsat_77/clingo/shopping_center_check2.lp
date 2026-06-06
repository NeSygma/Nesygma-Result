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

% Check each option independently
could_a :- assign(opt, 5).
could_b :- assign(pharm, 1).
could_c :- has_restaurant(3).
could_d :- assign(toy, 6).
could_e :- assign(vet, 4).

% Track which options are possible across all models
possible_a :- could_a.
possible_b :- could_b.
possible_c :- could_c.
possible_d :- could_d.
possible_e :- could_e.

#show possible_a/0.
#show possible_b/0.
#show possible_c/0.
#show possible_d/0.
#show possible_e/0.
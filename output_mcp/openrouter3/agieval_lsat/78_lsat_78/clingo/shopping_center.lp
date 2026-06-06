% Spaces
space(1..7).

% Businesses
business(optometrist).
business(pharmacy).
business(restaurant1).
business(restaurant2).
business(shoe_store).
business(toy_store).
business(veterinarian).

% Assignment: each business to exactly one space
1 { assigned(B, S) : space(S) } 1 :- business(B).

% Veterinarian fixed at space 5
assigned(veterinarian, 5).

% Constraint 1: Pharmacy at one end
:- assigned(pharmacy, S), S != 1, S != 7.

% Constraint 2: One restaurant at the other end
% Define which end pharmacy is at
pharmacy_at_1 :- assigned(pharmacy, 1).
pharmacy_at_7 :- assigned(pharmacy, 7).

% If pharmacy at 1, restaurant must be at 7
:- pharmacy_at_1, not (assigned(restaurant1, 7) ; assigned(restaurant2, 7)).
% If pharmacy at 7, restaurant must be at 1
:- pharmacy_at_7, not (assigned(restaurant1, 1) ; assigned(restaurant2, 1)).

% Constraint 3: Two restaurants separated by at least 2 other businesses
% |R1 - R2| >= 3 (since at least 2 businesses between means distance >= 3)
:- assigned(restaurant1, S1), assigned(restaurant2, S2), S1 < S2, S2 - S1 < 3.
:- assigned(restaurant1, S1), assigned(restaurant2, S2), S2 < S1, S1 - S2 < 3.

% Constraint 4: Pharmacy next to either optometrist or veterinarian
% Next means |S1 - S2| = 1
% We need to check if pharmacy is next to optometrist OR next to veterinarian
% Let's define helper predicates
next_to_optometrist :- assigned(pharmacy, SP), assigned(optometrist, SO), (SO = SP + 1; SO = SP - 1).
next_to_veterinarian :- assigned(pharmacy, SP), assigned(veterinarian, SV), (SV = SP + 1; SV = SP - 1).
:- not next_to_optometrist, not next_to_veterinarian.

% Constraint 5: Toy store cannot be next to veterinarian
% Veterinarian is at 5, so toy store cannot be at 4 or 6
:- assigned(toy_store, 4).
:- assigned(toy_store, 6).

% Answer choices conditions
% (A) The optometrist is in space 2
optometrist_in_2 :- assigned(optometrist, 2).

% (B) The pharmacy is in space 7
pharmacy_in_7 :- assigned(pharmacy, 7).

% (C) A restaurant is in space 4
restaurant_in_4 :- assigned(restaurant1, 4); assigned(restaurant2, 4).

% (D) The shoe store is in space 6
shoe_store_in_6 :- assigned(shoe_store, 6).

% (E) The toy store is in space 3
toy_store_in_3 :- assigned(toy_store, 3).

% Map the correct answer to option/1
% We need to find which condition holds in ALL valid solutions
% Since we want "must be true", we check if the condition is true in every answer set
% We'll use a different approach: check which option is true in the current model
% Since we're looking for what must be true, we need to see which condition is always true
% We can do this by checking if the negation of the condition is incompatible with constraints

% For "must be true", we can check if the condition is true in all valid assignments
% We'll add constraints to force each option to be false and see if it's still satisfiable
% But we can't do that in a single run...

% Better approach: Since we want the answer that MUST be true, we can check
% which condition is true in ALL answer sets. We can do this by ensuring
% that if the condition is false, the constraints are violated.

% Actually, let's think differently: We'll run the solver with the given constraints
% and see which of the answer choices is true in the resulting model(s)
% Since the problem asks "which must be true", and we have V=5 fixed,
% we can find all valid assignments and see which condition is always true

% For now, let's just derive the options based on the current model
% and we'll see what the solver gives us

option(a) :- optometrist_in_2.
option(b) :- pharmacy_in_7.
option(c) :- restaurant_in_4.
option(d) :- shoe_store_in_6.
option(e) :- toy_store_in_3.

#show option/1.
#show assigned/2.
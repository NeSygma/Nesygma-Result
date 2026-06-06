% Entities
fof(fluffy, axiom, cat(fluffy)).
fof(olive_garden, axiom, managed(olive_garden)).

% Cats are pets
fof(cat_pet, axiom, ! [X] : (cat(X) => pet(X))).

% Some managed building allows pets
fof(some_allows, axiom, ? [B] : (managed(B) & allows_pets(B))).

% If managed building allows pets, anyone can move in with a pet there
fof(pet_allowed, axiom, ! [B, P, A] :
    ((managed(B) & allows_pets(B) & pet(A))
     => allowed_with_pet(P, A, B))).

% Olive Garden rent is r2000
fof(og_rent, axiom, rent(olive_garden, r2000)).

% Deposit >= rent for managed buildings
fof(deposit_rule, axiom, ! [B, R] :
    ((managed(B) & rent(B, R)) => deposit(B, R))).

% r2000 > r1500
fof(rent_high, axiom, greater(r2000, r1500)).

% If deposit >= X and X > Y, then deposit > Y (not <= Y)
fof(deposit_above, axiom, ! [B, X, Y] :
    ((deposit(B, X) & greater(X, Y)) => ~deposit_le(B, Y))).

% Tom will rent if allowed with pet and deposit <= r1500
fof(tom_rent, axiom, ! [B] :
    ((managed(B) & allowed_with_pet(tom, fluffy, B) & deposit_le(B, r1500))
     => will_rent(tom, B))).

% Negated conclusion: Tom NOT allowed to move into Olive Garden with Fluffy
fof(goal_neg, conjecture, ~allowed_with_pet(tom, fluffy, olive_garden)).
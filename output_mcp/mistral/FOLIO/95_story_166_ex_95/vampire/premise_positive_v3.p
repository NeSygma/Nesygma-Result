% Managed building and pet ontology (corrected types)

% Types: all entities are individuals ($i)

% Constants
tff(olive_garden, type, olive_garden: $i).
tff(fluffy, type, fluffy: $i).
tff(tom, type, tom: $i).

% Predicates
tff(managed_building, type, managed_building: $i > $o).
tff(pet, type, pet: $i > $o).
tff(cat, type, cat: $i > $o).
tff(owner, type, owner: ($i * $i) > $o).
tff(allows_pets, type, allows_pets: $i > $o).
tff(can_move_in_with_pet, type, can_move_in_with_pet: ($i * $i) > $o).
tff(rent_apartment, type, rent_apartment: ($i * $i) > $o).

% Functions for rent and security deposit (interpreted as constants for the Olive Garden)
tff(rent, type, rent: $i > $int).
tff(security_deposit, type, security_deposit: $i > $int).

% Predicates for arithmetic
tff(greater, type, greater: ($int * $int) > $o).
tff(less_equal, type, less_equal: ($int * $int) > $o).

% Premise: Pets are allowed in some managed buildings.
fof(some_building_allows_pets, axiom, ? [B: $i] : (managed_building(B) & allows_pets(B))).

% Premise: The security deposit can be either equal to the monthly rent at a managed building or more.
fof(deposit_rule, axiom, ! [B: $i] :
    (managed_building(B) =>
        (security_deposit(B) = rent(B) | greater(security_deposit(B), rent(B))))).

% Premise: Fluffy is Tom's cat.
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(fluffy_owner, axiom, owner(fluffy, tom)).

% Premise: Cats are pets.
fof(cats_are_pets, axiom, ! [X: $i] : (cat(X) => pet(X))).

% Premise: The Olive Garden is a managed building.
fof(olive_garden_managed, axiom, managed_building(olive_garden)).

% Premise: The monthly rent at the Olive Garden is $2000.
fof(olive_garden_rent, axiom, rent(olive_garden) = 2000).

% Premise: $2000 is more than $1500.
fof(2000_gt_1500, axiom, greater(2000, 1500)).

% Premise: If a managed building allows pets, then people are allowed to move in with a pet.
fof(allow_pets_rule, axiom, ! [B: $i, P: $i, Pet: $i] :
    (managed_building(B) & allows_pets(B) => can_move_in_with_pet(P, Pet))).

% Premise: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
fof(tom_rent_condition, axiom, ! [B: $i] :
    (managed_building(B) =>
        (can_move_in_with_pet(tom, fluffy) & less_equal(security_deposit(B), 1500) => rent_apartment(B, tom)))).

% Conclusion to evaluate: The security deposit at the Olive Garden is either $2000 or more.
fof(conclusion, conjecture, 
    (security_deposit(olive_garden) = 2000 | greater(security_deposit(olive_garden), 2000))).
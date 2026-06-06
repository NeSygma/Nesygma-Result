% Managed building and pet ontology with arithmetic (negation of conclusion)

% Types
tff(managed_building_type, type, managed_building: $tType).
tff(olive_garden, type, olive_garden: managed_building).

tff(pet_type, type, pet: $tType).
tff(fluffy, type, fluffy: pet).

tff(person_type, type, person: $tType).
tff(tom, type, tom: person).

tff(cat_type, type, cat: $tType).

% Functions for rent and security deposit
tff(rent_func, type, rent: managed_building > $int).
tff(security_deposit_func, type, security_deposit: managed_building > $int).

% Predicates
tff(allows_pets, type, allows_pets: managed_building > $o).
tff(cat, type, cat: pet > $o).
tff(pet, type, pet: pet > $o).
tff(owner, type, owner: (pet * person) > $o).
tff(can_move_in_with_pet, type, can_move_in_with_pet: (person * pet) > $o).
tff(rent_apartment, type, rent_apartment: (managed_building * person) > $o).
tff(greater, type, greater: ($int * $int) > $o).
tff(less_equal, type, less_equal: ($int * $int) > $o).

% Premise: Pets are allowed in some managed buildings.
fof(some_building_allows_pets, axiom, ? [B: managed_building] : allows_pets(B)).

% Premise: The security deposit can be either equal to the monthly rent at a managed building or more.
fof(deposit_rule, axiom, ! [B: managed_building] :
    (security_deposit(B) = rent(B) | greater(security_deposit(B), rent(B)))).

% Premise: Fluffy is Tom's cat.
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(fluffy_owner, axiom, owner(fluffy, tom)).

% Premise: Cats are pets.
fof(cats_are_pets, axiom, ! [X: pet] : (cat(X) => pet(X))).

% Premise: The Olive Garden is a managed building.
fof(olive_garden_managed, axiom, managed_building(olive_garden)).

% Premise: The monthly rent at the Olive Garden is $2000.
fof(olive_garden_rent, axiom, rent(olive_garden) = 2000).

% Premise: $2000 is more than $1500.
fof(2000_gt_1500, axiom, greater(2000, 1500)).

% Premise: If a managed building allows pets, then people are allowed to move in with a pet.
fof(allow_pets_rule, axiom, ! [B: managed_building, P: person, Pet: pet] :
    (allows_pets(B) => can_move_in_with_pet(P, Pet))).

% Premise: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
fof(tom_rent_condition, axiom, ! [B: managed_building] :
    (can_move_in_with_pet(tom, fluffy) & less_equal(security_deposit(B), 1500) => rent_apartment(B, tom))).

% Negation of the conclusion: The security deposit at the Olive Garden is NOT either $2000 or more.
fof(conclusion_negation, conjecture, 
    ~(security_deposit(olive_garden) = 2000 | greater(security_deposit(olive_garden), 2000))).
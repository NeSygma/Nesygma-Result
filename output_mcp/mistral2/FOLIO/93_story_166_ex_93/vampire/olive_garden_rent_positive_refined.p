tff(managed_building_type, type, managed_building: $tType).
tff(person_type, type, person: $tType).
tff(animal_type, type, animal: $tType).

% Constants

%% Managed buildings
fof(olive_garden_decl, axiom, olive_garden: managed_building).

%% People
fof(tom_decl, axiom, tom: person).

%% Animals
fof(fluffy_decl, axiom, fluffy: animal).

% Predicates

tff(pets_allowed_type, type, pets_allowed: managed_building > $o).
tff(deposit_required_type, type, deposit_required: managed_building > $o).
tff(security_deposit_type, type, security_deposit: (managed_building * $int) > $o).
tff(rent_value_type, type, rent_value: (managed_building * $int) > $o).
tff(more_than_type, type, more_than: ($int * $int) > $o).
tff(less_or_equal_type, type, less_or_equal: ($int * $int) > $o).
tff(owns_type, type, owns: (person * animal) > $o).
tff(cat_type, type, cat: animal > $o).
tff(pet_type, type, pet: animal > $o).
tff(allowed_with_pet_type, type, allowed_with_pet: (person * managed_building) > $o).
tff(will_rent_type, type, will_rent: (person * managed_building) > $o).

% Axioms

fof(pets_allowed_some, axiom, ? [X: managed_building] : pets_allowed(X)).
fof(deposit_required_managed, axiom, ! [X: managed_building] : deposit_required(X)).
fof(deposit_relation, axiom, ! [X: managed_building, D: $int, R: $int] : ( (security_deposit(X, D) & rent_value(X, R)) => ( less_or_equal(D, R) | more_than(D, R) ) )).
fof(fluffy_is_toms_cat, axiom, owns(tom, fluffy)).
fof(cats_are_pets, axiom, ! [C: animal] : (cat(C) => pet(C))).
fof(olive_garden_rent_value, axiom, rent_value(olive_garden, 2000)).
fof(2000_more_than_1500, axiom, more_than(2000, 1500)).
fof(allowed_with_pet_rule, axiom, ! [X: managed_building, P: person, C: animal] : ( (pets_allowed(X) & owns(P, C) & cat(C)) => allowed_with_pet(P, X) )).
fof(tom_rent_condition, axiom, ! [X: managed_building, D: $int] : ( (allowed_with_pet(tom, X) & security_deposit(X, D) & less_or_equal(D, 1500)) => will_rent(tom, X) )).

% Facts

fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(pets_allowed_olive_garden, axiom, pets_allowed(olive_garden)).
fof(olive_garden_deposit, axiom, security_deposit(olive_garden, 2000)).
fof(fluffy_is_pet, axiom, pet(fluffy)).

% Goal

fof(goal, conjecture, will_rent(tom, olive_garden)).
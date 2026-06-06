fof(managed_building_olive_garden, axiom, managed_building(olive_garden)).
fof(pets_allowed_some, axiom, ? [X] : (managed_building(X) & pets_allowed(X))).
fof(deposit_required_managed, axiom, ! [X] : (managed_building(X) => deposit_required(X))).
fof(deposit_relation, axiom, ! [X, D, R] : ((managed_building(X) & security_deposit(X, D) & rent_value(X, R)) => (deposit_ge_rent(X, D) | more_than(D, R)))).
fof(fluffy_is_toms_cat, axiom, owns(tom, fluffy)).
fof(cats_are_pets, axiom, ! [C] : (cat(C) => pet(C))).
fof(olive_garden_rent_value, axiom, rent_value(olive_garden, 2000)).
fof(2000_more_than_1500, axiom, more_than(2000, 1500)).
fof(allowed_with_pet_rule, axiom, ! [X, P, C] : ((managed_building(X) & pets_allowed(X) & owns(P, C) & cat(C)) => allowed_with_pet(P, X))).
fof(tom_rent_condition, axiom, ! [X, D] : ((managed_building(X) & allowed_with_pet(tom, X) & security_deposit(X, D) & deposit_ge_rent(X, D) & less_or_equal(D, 1500)) => will_rent(tom, X))).

fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(pets_allowed_olive_garden, axiom, pets_allowed(olive_garden)).
fof(olive_garden_deposit, axiom, security_deposit(olive_garden, 2000)).
fof(fluffy_is_pet, axiom, pet(fluffy)).

fof(goal, conjecture, will_rent(tom, olive_garden)).
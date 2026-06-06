fof(managed_building_olive_garden, axiom, managed_building(olive_garden)).
fof(pets_allowed_some, axiom, ? [X] : (managed_building(X) & pets_allowed(X))).
fof(deposit_required_managed, axiom, ! [X] : (managed_building(X) => deposit_required(X))).
fof(deposit_relation, axiom, ! [X, D, R] : ((managed_building(X) & security_deposit(X, D) & monthly_rent(X, R)) => (D = R | more_than(D, R)))).
fof(fluffy_is_toms_cat, axiom, owns(tom, fluffy)).
fof(cats_are_pets, axiom, ! [C] : (cat(C) => pet(C))).
fof(olive_garden_rent, axiom, monthly_rent(olive_garden, 2000)).
fof(2000_more_than_1500, axiom, more_than(2000, 1500)).
fof(allowed_with_pet_rule, axiom, ! [X, P, C] : ((managed_building(X) & pets_allowed(X) & owns(P, C) & cat(C)) => allowed_with_pet(P, X))).
fof(tom_rent_condition, axiom, ! [X] : ((managed_building(X) & allowed_with_pet(tom, X) & security_deposit(X, D) & (D = 2000 | more_than(D, 2000)) & ~more_than(D, 1500)) => will_rent(tom, X))).

fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(pets_allowed_olive_garden, axiom, pets_allowed(olive_garden)).

fof(goal_negation, conjecture, ~will_rent(tom, olive_garden)).
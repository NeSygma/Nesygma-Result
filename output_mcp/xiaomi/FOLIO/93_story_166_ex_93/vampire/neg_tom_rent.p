fof(cat_is_pet, axiom, ! [X] : (cat(X) => pet(X))).
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(fluffy_is_toms_cat, axiom, owner(fluffy, tom)).
fof(olive_garden_managed, axiom, managed_building(olive_garden)).
fof(some_managed_allow_pets, axiom, ? [B] : (managed_building(B) & allows_pets(B))).
fof(deposit_required, axiom, ! [B] : (managed_building(B) => deposit_required(B))).
fof(deposit_ge_rent, axiom, ! [B,R,D] : ((managed_building(B) & rent_amount(B,R) & deposit_amount(B,D)) => more_than_eq(D,R))).
fof(rent_olive_garden, axiom, rent_amount(olive_garden, amount_2000)).
fof(more_2000_1500, axiom, more_than(amount_2000, amount_1500)).
fof(more_than_implies_more_eq, axiom, ! [X,Y] : (more_than(X,Y) => more_than_eq(X,Y))).
fof(more_than_trans, axiom, ! [X,Y,Z] : ((more_than_eq(X,Y) & more_than(Y,Z)) => more_than(X,Z))).
fof(allows_pets_implies_allowed, axiom, ! [B,P,Pet] : ((managed_building(B) & allows_pets(B) & pet(Pet)) => allowed_to_move_in(P, Pet, B))).
fof(tom_rents_condition, axiom, ! [B] : ((allowed_to_move_in(tom, fluffy, B) & ? [D] : (deposit_amount(B,D) & more_than_eq(amount_1500, D))) => will_rent(tom, B))).
fof(goal, conjecture, ~will_rent(tom, olive_garden)).
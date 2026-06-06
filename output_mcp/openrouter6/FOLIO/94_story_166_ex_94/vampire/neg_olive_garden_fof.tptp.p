fof(managed_building_olive, axiom, managed_building(olive_garden)).
fof(pets_allowed_some, axiom, ? [B] : (managed_building(B) & pets_allowed_in(B))).
fof(deposit_required, axiom, ! [B] : (managed_building(B) => deposit_required(B))).
fof(security_deposit_at_least_rent, axiom, ! [B, D, R] : ((managed_building(B) & security_deposit(B, D) & monthly_rent(B, R)) => (greater_than(D, R) | D = R))).
fof(cat_of_tom, axiom, cat_of(tom, fluffy)).
fof(cats_are_pets, axiom, ! [A] : (cat(A) => pet(A))).
fof(monthly_rent_olive, axiom, monthly_rent(olive_garden, n2000)).
fof(greater_2000_1500, axiom, greater_than(n2000, n1500)).
fof(tom_rent_condition, axiom, ! [B, D] : ((managed_building(B) & allowed_to_move_in(tom, B, fluffy) & security_deposit(B, D) & (greater_than(n1500, D) | D = n1500)) => rent_apartment(tom, B))).
fof(pets_allowed_implies_move_in, axiom, ! [B, P, A] : ((managed_building(B) & pets_allowed_in(B) & pet(A)) => allowed_to_move_in(P, B, A))).
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(neg_goal, conjecture, ~allowed_to_move_in(tom, olive_garden, fluffy)).
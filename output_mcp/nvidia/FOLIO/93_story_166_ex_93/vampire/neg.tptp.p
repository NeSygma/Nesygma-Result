fof(exists_building_with_pets, axiom, ? [B] : (managed_building(B) & allows_pets(B))).
fof(pet_allowed_rule, axiom, ! [B,P] : (allows_pets(B) => allowed_to_move_in_with_pet(P, B))).
fof(fact_fluffy_cat, axiom, cat(fluffy)).
fof(cat_implies_pet, axiom, ! [X] : (cat(X) => pet(X))).
fof(fact_olive_garden_managed, axiom, managed_building(olive_garden)).
fof(rent_condition_rule, axiom, ! [B] : ((managed_building(B) & allowed_to_move_in_with_fluffy & security_deposit_le_1500) => rent(tom, B))).
fof(goal, conjecture, ~rent(tom, olive_garden)).
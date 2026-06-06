fof(distinct, axiom, (tom != fluffy & tom != olive_garden & fluffy != olive_garden & tom != b1 & fluffy != b1 & olive_garden != b1)).
fof(cat_fluffy, axiom, cat(fluffy)).
fof(cat_implies_pet, axiom, ![X] : (cat(X) => pet(X))).
fof(pet_fluffy, axiom, pet(fluffy)).
fof(managed_olive, axiom, managed_building(olive_garden)).
fof(managed_b1, axiom, managed_building(b1)).
fof(allows_pets_b1, axiom, allows_pets(b1)).
fof(exists_allows_pets, axiom, ?[B] : (managed_building(B) & allows_pets(B))).
fof(rule_allowed, axiom, ![P, Pet, B] : ((managed_building(B) & allows_pets(B)) => allowed_to_move_in_with_pet(P, Pet, B))).
fof(goal, conjecture, allowed_to_move_in_with_pet(tom, fluffy, olive_garden)).
fof(managed_building_def, axiom, managed_building(olive_garden)).
fof(pet_def, axiom, pet(fluffy)).
fof(cat_def, axiom, cat(fluffy)).
fof(is_cat_of_def, axiom, is_cat_of(fluffy, tom)).
fof(cat_is_pet, axiom, ! [C] : (cat(C) => pet(C))).
fof(monthly_rent_def, axiom, monthly_rent(olive_garden, 2000)).
fof(more_than_def, axiom, more_than(2000, 1500)).
fof(allows_pets_somewhere, axiom, ? [B, P] : (managed_building(B) & pet(P) & allows_pets(B, P))).
fof(requires_deposit, axiom, ! [B] : (managed_building(B) => ? [D] : requires_deposit(B, D))).
fof(deposit_condition, axiom, ! [B, D] : (requires_deposit(B, D) => (D = monthly_rent(B) | more_than(D, monthly_rent(B))))).
fof(allowed_to_move_in_with_pet_def, axiom, ! [B, P, Person] : (allows_pets(B, P) => allowed_to_move_in_with_pet(Person, P))).
fof(will_rent_condition, axiom, ! [B] : (managed_building(B) => (will_rent(tom, B) <=> (allowed_to_move_in_with_pet(tom, fluffy) & security_deposit_le(B, 1500))))).

fof(goal, conjecture, allowed_to_move_in_with_pet(tom, fluffy)).
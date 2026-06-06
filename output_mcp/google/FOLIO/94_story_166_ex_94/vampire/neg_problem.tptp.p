tff(managed_type, type, managed: $i > $o).
tff(cat_type, type, cat: $i > $o).
tff(pet_type, type, pet: $i > $o).
tff(allows_pets_type, type, allows_pets: $i > $o).
tff(allowed_with_pet_type, type, allowed_with_pet: $i > $o).
tff(allowed_with_fluffy_type, type, allowed_with_fluffy: ($i * $i) > $o).
tff(monthly_rent_type, type, monthly_rent: $i > $int).
tff(security_deposit_type, type, security_deposit: $i > $int).
tff(olive_garden_decl, type, olive_garden: $i).
tff(tom_decl, type, tom: $i).
tff(fluffy_decl, type, fluffy: $i).

tff(managed_og, axiom, managed(olive_garden)).
tff(cat_fluffy, axiom, cat(fluffy)).
tff(cat_is_pet, axiom, ! [X: $i] : (cat(X) => pet(X))).
tff(some_managed_allow_pets, axiom, ? [B: $i] : (managed(B) & allows_pets(B))).
tff(managed_deposit_ge_rent, axiom, ! [B: $i] : (managed(B) => $greatereq(security_deposit(B), monthly_rent(B)))).
tff(rent_og, axiom, monthly_rent(olive_garden) = 2000).
tff(rent_comparison, axiom, $greater(2000, 1500)).
tff(pet_rule, axiom, ! [B: $i] : ((managed(B) & allows_pets(B)) => allowed_with_pet(B))).
tff(tom_rule, axiom, ! [B: $i] : (allowed_with_pet(B) => allowed_with_fluffy(tom, B))).
tff(goal, conjecture, ~allowed_with_fluffy(tom, olive_garden)).
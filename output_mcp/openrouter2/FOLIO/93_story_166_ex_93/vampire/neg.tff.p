tff(person_sort, type, person: $tType).
tff(pet_sort, type, pet: $tType).
tff(building_sort, type, building: $tType).
tff(olive_garden_decl, type, olive_garden: building).
tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: pet).
tff(2000_decl, type, 2000: $int).
tff(1500_decl, type, 1500: $int).
tff(managed_building_decl, type, managed_building: building > $o).
tff(allows_pets_decl, type, allows_pets: building > $o).
tff(pet_decl, type, pet: pet > $o).
tff(cat_decl, type, cat: pet > $o).
tff(allowed_to_move_in_with_pet_decl, type, allowed_to_move_in_with_pet: (person * pet * building) > $o).
tff(rent_apartment_decl, type, rent_apartment: (person * building) > $o).
tff(deposit_required_decl, type, deposit_required: building > $o).
tff(monthly_rent_decl, type, monthly_rent: building > $int).
tff(security_deposit_decl, type, security_deposit: building > $int).
% Axioms
fof(cat_implies_pet, axiom, ! [X: pet] : (cat(X) => pet(X))).
fof(fluffy_cat, axiom, cat(fluffy)).
fof(pet_fluffy, axiom, pet(fluffy)).
fof(olive_garden_managed, axiom, managed_building(olive_garden)).
fof(monthly_rent_olive, axiom, monthly_rent(olive_garden) = 2000).
fof(security_ge_monthly, axiom, $greatereq(security_deposit(olive_garden), monthly_rent(olive_garden))).
fof(deposit_required_olive, axiom, deposit_required(olive_garden)).
fof(2000_gt_1500, axiom, $greater(2000, 1500)).
fof(move_in_rule, axiom, ! [B: building, P: person, Pet: pet] : (managed_building(B) & allows_pets(B) => allowed_to_move_in_with_pet(P, Pet, B))).
fof(rent_rule, axiom, ! [B: building] : (allowed_to_move_in_with_pet(tom, fluffy, B) & $lesseq(security_deposit(B), 1500) => rent_apartment(tom, B))).
fof(pets_allowed_some, axiom, ? [B: building] : (managed_building(B) & allows_pets(B))).
% Conjecture: Tom will NOT rent an apartment in Olive Garden
fof(goal, conjecture, ~rent_apartment(tom, olive_garden)).
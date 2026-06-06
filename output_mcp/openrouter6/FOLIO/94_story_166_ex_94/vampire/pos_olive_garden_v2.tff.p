tff(building_sort, type, building: $tType).
tff(person_sort, type, person: $tType).
tff(animal_sort, type, animal: $tType).
tff(olive_garden_const, type, olive_garden: building).
tff(tom_const, type, tom: person).
tff(fluffy_const, type, fluffy: animal).
tff(managed_building_pred, type, managed_building: (building) > $o).
tff(pets_allowed_in_pred, type, pets_allowed_in: (building) > $o).
tff(deposit_required_pred, type, deposit_required: (building) > $o).
tff(monthly_rent_pred, type, monthly_rent: (building, $int) > $o).
tff(security_deposit_pred, type, security_deposit: (building, $int) > $o).
tff(cat_pred, type, cat: (animal) > $o).
tff(pet_pred, type, pet: (animal) > $o).
tff(cat_of_pred, type, cat_of: (person, animal) > $o).
tff(allowed_to_move_in_pred, type, allowed_to_move_in: (person, building, animal) > $o).
tff(rent_apartment_pred, type, rent_apartment: (person, building) > $o).
tff(premise1, axiom, ? [B: building] : (managed_building(B) & pets_allowed_in(B))).
tff(premise2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).
tff(premise3, axiom, ! [B: building, D: $int, R: $int] : ((managed_building(B) & security_deposit(B, D) & monthly_rent(B, R)) => $greatereq(D, R))).
tff(premise4, axiom, cat_of(tom, fluffy)).
tff(premise5, axiom, ! [A: animal] : (cat(A) => pet(A))).
tff(premise6, axiom, managed_building(olive_garden)).
tff(premise7, axiom, monthly_rent(olive_garden, 2000)).
tff(premise8, axiom, $greater(2000, 1500)).
tff(premise9, axiom, ! [B: building, D: $int] : ((managed_building(B) & allowed_to_move_in(tom, B, fluffy) & security_deposit(B, D) & $lesseq(D, 1500)) => rent_apartment(tom, B))).
tff(premise10, axiom, ! [B: building, P: person, A: animal] : ((managed_building(B) & pets_allowed_in(B) & pet(A)) => allowed_to_move_in(P, B, A))).
tff(fluffy_is_cat, axiom, cat(fluffy)).
tff(conclusion, conjecture, allowed_to_move_in(tom, olive_garden, fluffy)).
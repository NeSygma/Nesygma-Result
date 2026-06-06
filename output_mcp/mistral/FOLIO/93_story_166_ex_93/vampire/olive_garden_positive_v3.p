tff(person_type, type, person: $tType).
tff(pet_type, type, pet: $tType).
tff(building_type, type, building: $tType).

tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: pet).
tff(olive_garden_decl, type, olive_garden: building).

tff(is_pet_of_type, type, is_pet_of: (pet * person) > $o).
tff(cat_type, type, cat: pet > $o).
tff(pet_type_pred, type, pet: pet > $o).
tff(managed_building_type, type, managed_building: building > $o).
tff(allows_pets_type, type, allows_pets: building > $o).
tff(rent_type, type, rent: (building * $int) > $o).
tff(deposit_required_type, type, deposit_required: (building * $int) > $o).
tff(can_move_in_with_type, type, can_move_in_with: (person * pet * building) > $o).
tff(will_rent_type, type, will_rent: (person * building) > $o).

fof(fluffy_is_toms_cat, axiom, is_pet_of(fluffy, tom)).
fof(cats_are_pets, axiom, ! [X: pet] : (cat(X) => pet(X))).
fof(fluffy_is_cat, axiom, cat(fluffy)).
fof(olive_garden_managed, axiom, managed_building(olive_garden)).
fof(olive_garden_rent, axiom, rent(olive_garden, 2000)).

fof(twenty_hundred_gt_fifteen_hundred, axiom, 2000 > 1500).

fof(pets_allowed_some_managed, axiom, ? [B: building] : (managed_building(B) & allows_pets(B))).
fof(deposit_required_for_managed, axiom, ! [B: building] : (managed_building(B) => ? [D: $int] : deposit_required(B, D))).
fof(deposit_rule, axiom, ! [B: building, D: $int, R: $int] : ((deposit_required(B, D) & rent(B, R)) => (D = R | D > R))).
fof(tom_rent_condition, axiom, ! [B: building] : ((can_move_in_with(tom, fluffy, B) & ? [D: $int] : (deposit_required(B, D) & D =< 1500)) => will_rent(tom, B))).
fof(allows_pets_implies_can_move_in, axiom, ! [B: building, P: pet, Person: person] : (allows_pets(B) => can_move_in_with(Person, P, B))).

fof(conclusion, conjecture, will_rent(tom, olive_garden)).
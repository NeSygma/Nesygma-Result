tff(building_type, type, building: $tType).
tff(person_type, type, person: $tType).
tff(pet_type, type, pet: $tType).

tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: pet).
tff(olive_garden_decl, type, olive_garden: building).

tff(managed_building_decl, type, managed_building: building > $o).
tff(allows_pets_decl, type, allows_pets: building > $o).
tff(deposit_required_decl, type, deposit_required: building > $o).
tff(monthly_rent_decl, type, monthly_rent: (building * $int) > $o).
tff(cat_decl, type, cat: pet > $o).
tff(pet_decl, type, pet: pet > $o).
tff(owns_decl, type, owns: (person * pet) > $o).
tff(apartment_in_decl, type, apartment_in: (person * building) > $o).
tff(can_move_in_with_decl, type, can_move_in_with: (person * pet * building) > $o).
tff(allows_move_in_with_decl, type, allows_move_in_with: (building * person * pet) > $o).

% Premise 1: Pets are allowed in some managed buildings
tff(premise_1, axiom, ? [B: building] : (managed_building(B) & allows_pets(B))).

% Premise 2: Deposit required for apartments in managed buildings
tff(premise_2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).

% Premise 3: Security deposit can be equal to or more than monthly rent
tff(premise_3, axiom, 
    ! [B: building, R: $int] : 
    (deposit_required(B) & monthly_rent(B, R) => $greatereq(R, 2000))).

% Premise 4: Fluffy is Tom's cat
tff(premise_4, axiom, owns(tom, fluffy)).
tff(premise_4b, axiom, cat(fluffy)).

% Premise 5: Cats are pets
tff(premise_5, axiom, ! [P: pet] : (cat(P) => pet(P))).

% Premise 6: Olive Garden is a managed building
tff(premise_6, axiom, managed_building(olive_garden)).

% Premise 7: Monthly rent at Olive Garden is $2000
tff(premise_7, axiom, monthly_rent(olive_garden, 2000)).

% Premise 8: $2000 > $1500 (arithmetic fact)
tff(premise_8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent if allowed to move in with Fluffy AND deposit ≤ $1500
tff(premise_9, axiom, 
    (can_move_in_with(tom, fluffy, olive_garden) & $lesseq(2000, 1500))
    => apartment_in(tom, olive_garden)).

% Premise 10: If building allows pets, then people can move in with pets
tff(premise_10, axiom, 
    ! [B: building, P: pet, Person: person] : 
    (allows_pets(B) & pet(P) => allows_move_in_with(B, Person, P))).

% Additional fact: Tom can move in if the building allows it
tff(tom_can_move, axiom, 
    ! [B: building, P: pet] : 
    (allows_move_in_with(B, tom, P) => can_move_in_with(tom, P, B))).

% Conclusion negation: Tom will NOT rent an apartment in The Olive Garden
tff(goal_neg, conjecture, ~apartment_in(tom, olive_garden)).
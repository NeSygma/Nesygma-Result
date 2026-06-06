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

% Premise 1: Pets are allowed in some managed buildings
tff(premise_1, axiom, ? [B: building] : (managed_building(B) & allows_pets(B))).

% Premise 2: Deposit required for apartments in managed buildings
tff(premise_2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).

% Premise 3: Security deposit can be equal to or more than monthly rent
% We'll model this as: if deposit is required, then deposit >= rent
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
% Since deposit ≥ rent = $2000, deposit ≤ $1500 is impossible
% So Tom will NOT rent based on this condition
tff(premise_9, axiom, 
    ! [B: building] : 
    (managed_building(B) & deposit_required(B) & monthly_rent(B, 2000) 
     => ~apartment_in(tom, B))).

% Premise 10: If building allows pets, then people can move in with pets
tff(premise_10, axiom, 
    ! [B: building] : 
    (allows_pets(B) => managed_building(B))).

% Conclusion: Tom will rent an apartment in The Olive Garden
tff(goal, conjecture, apartment_in(tom, olive_garden)).
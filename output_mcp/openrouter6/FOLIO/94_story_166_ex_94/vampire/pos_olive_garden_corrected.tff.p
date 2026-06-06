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

% Premise 1: Pets are allowed in some managed buildings.
tff(premise1, axiom, ? [B: building] : (managed_building(B) & pets_allowed_in(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(premise2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
% This means for any managed building, the security deposit is at least the monthly rent.
tff(premise3, axiom, ! [B: building, D: $int, R: $int] : 
    ((managed_building(B) & security_deposit(B, D) & monthly_rent(B, R)) => $greatereq(D, R))).

% Premise 4: Fluffy is Tom's cat.
tff(premise4, axiom, cat_of(tom, fluffy)).

% Premise 5: Cats are pets.
tff(premise5, axiom, ! [A: animal] : (cat(A) => pet(A))).

% Premise 6: The Olive Garden is a managed building.
tff(premise6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(premise7, axiom, monthly_rent(olive_garden, 2000)).

% Premise 8: $2000 is more than $1500.
tff(premise8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
tff(premise9, axiom, ! [B: building, D: $int] : 
    ((managed_building(B) & allowed_to_move_in(tom, B, fluffy) & security_deposit(B, D) & $lesseq(D, 1500)) 
     => rent_apartment(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
tff(premise10, axiom, ! [B: building, P: person, A: animal] : 
    ((managed_building(B) & pets_allowed_in(B) & pet(A)) => allowed_to_move_in(P, B, A))).

% Additional fact: Fluffy is a cat.
tff(fluffy_is_cat, axiom, cat(fluffy)).

% Conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.
tff(conclusion, conjecture, allowed_to_move_in(tom, olive_garden, fluffy)).
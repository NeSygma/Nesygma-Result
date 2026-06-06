tff(building_type, type, building: $tType).
tff(person_type, type, person: $tType).
tff(animal_type, type, animal: $tType).

tff(olive_garden_decl, type, olive_garden: building).
tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: animal).

tff(managed_building_decl, type, managed_building: $tType > $o).
tff(pets_allowed_in_decl, type, pets_allowed_in: $tType > $o).
tff(deposit_required_decl, type, deposit_required: $tType > $o).
tff(monthly_rent_decl, type, monthly_rent: (building * $int) > $o).
tff(security_deposit_decl, type, security_deposit: (building * $int) > $o).
tff(cat_decl, type, cat: $tType > $o).
tff(pet_decl, type, pet: $tType > $o).
tff(cat_of_decl, type, cat_of: (person * animal) > $o).
tff(allowed_to_move_in_decl, type, allowed_to_move_in: (person * building * animal) > $o).
tff(rent_apartment_decl, type, rent_apartment: (person * building) > $o).

% Premise 1: Pets are allowed in some managed buildings.
tff(premise1, axiom, ? [B: building] : (managed_building(B) & pets_allowed_in(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(premise2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
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

% Negated conclusion: Tom is NOT allowed to move into an apartment in The Olive Garden with Fluffy.
tff(neg_conclusion, conjecture, ~allowed_to_move_in(tom, olive_garden, fluffy)).
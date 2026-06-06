% Positive version: conjecture is "Tom will rent an apartment in The Olive Garden"
tff(building_type, type, building: $tType).
tff(person_type, type, person: $tType).
tff(animal_type, type, animal: $tType).

% Constants
tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: animal).
tff(olive_garden_decl, type, olive_garden: building).

% Predicates
tff(managed_building_decl, type, managed_building: building > $o).
tff(allows_pets_decl, type, allows_pets: building > $o).
tff(deposit_required_decl, type, deposit_required: building > $o).
tff(cat_decl, type, cat: animal > $o).
tff(pet_decl, type, pet: animal > $o).
tff(owns_decl, type, owns: (person * animal) > $o).
tff(allowed_move_in_with_decl, type, allowed_move_in_with: (person * animal * building) > $o).
tff(tom_rents_decl, type, tom_rents: (person * building) > $o).
tff(monthly_rent_decl, type, monthly_rent: building > $int).
tff(security_deposit_decl, type, security_deposit: building > $int).

% Premise 1: Pets are allowed in some managed buildings.
tff(p1, axiom, ? [B: building] : (managed_building(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(p2, axiom, ! [B: building] : (managed_building(B) => deposit_required(B))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
tff(p3, axiom, ! [B: building] : (managed_building(B) => (security_deposit(B) = monthly_rent(B) | $greater(security_deposit(B), monthly_rent(B))))).

% Premise 4: Fluffy is Tom's cat.
tff(p4, axiom, (cat(fluffy) & owns(tom, fluffy))).

% Premise 5: Cats are pets.
tff(p5, axiom, ! [A: animal] : (cat(A) => pet(A))).

% Premise 6: The Olive Garden is a managed building.
tff(p6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(p7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 8: $2000 is more than $1500.
tff(p8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
tff(p9, axiom, ! [B: building] : ((managed_building(B) & allowed_move_in_with(tom, fluffy, B) & $lesseq(security_deposit(B), 1500)) => tom_rents(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
tff(p10, axiom, ! [B: building] : ((managed_building(B) & allows_pets(B)) => ! [P: person, A: animal] : (pet(A) => allowed_move_in_with(P, A, B)))).

% Conclusion: Tom will rent an apartment in The Olive Garden.
tff(goal, conjecture, tom_rents(tom, olive_garden)).
tff(person_type, type, person: $tType).
tff(animal_type, type, animal: $tType).
tff(building_type, type, building: $tType).

tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: animal).
tff(olive_garden_decl, type, olive_garden: building).

tff(cat_decl, type, cat: animal > $o).
tff(pet_decl, type, pet: animal > $o).
tff(managed_building_decl, type, managed_building: building > $o).
tff(allows_pets_decl, type, allows_pets: building > $o).
tff(owns_decl, type, owns: (person * animal) > $o).
tff(allowed_to_move_in_with_decl, type, allowed_to_move_in_with: (person * animal * building) > $o).
tff(will_rent_decl, type, will_rent: (person * building) > $o).
tff(monthly_rent_decl, type, monthly_rent: building > $int).
tff(security_deposit_decl, type, security_deposit: building > $int).

% Premise 1: Pets are allowed in some managed buildings.
tff(premise_1, axiom,
    ? [B: building] : (managed_building(B) & allows_pets(B))).

% Premise 3: The security deposit >= monthly rent at a managed building.
tff(premise_3, axiom,
    ! [B: building] : (managed_building(B) => $greatereq(security_deposit(B), monthly_rent(B)))).

% Premise 4: Fluffy is Tom's cat.
tff(premise_4a, axiom, cat(fluffy)).
tff(premise_4b, axiom, owns(tom, fluffy)).

% Premise 5: Cats are pets.
tff(premise_5, axiom,
    ! [A: animal] : (cat(A) => pet(A))).

% Premise 6: The Olive Garden is a managed building.
tff(premise_6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(premise_7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 8: $2000 > $1500 is automatically true in $int.

% Premise 9: Tom will rent if allowed to move in with Fluffy AND deposit <= $1500.
tff(premise_9, axiom,
    ! [B: building] :
      ((managed_building(B) & allowed_to_move_in_with(tom, fluffy, B) & $lesseq(security_deposit(B), 1500))
       => will_rent(tom, B))).

% Premise 10: If a managed building allows pets, people can move in with a pet.
tff(premise_10, axiom,
    ! [P: person, A: animal, B: building] :
      ((managed_building(B) & allows_pets(B) & pet(A))
       => allowed_to_move_in_with(P, A, B))).

% Conclusion: Tom will rent an apartment in The Olive Garden.
tff(goal, conjecture, will_rent(tom, olive_garden)).
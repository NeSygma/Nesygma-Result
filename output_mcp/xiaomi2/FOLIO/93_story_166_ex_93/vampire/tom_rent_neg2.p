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
tff(allowed_to_move_in_with_decl, type, allowed_to_move_in_with: (person * animal * building) > $o).
tff(will_rent_decl, type, will_rent: (person * building) > $o).
tff(monthly_rent_decl, type, monthly_rent: building > $int).
tff(security_deposit_decl, type, security_deposit: building > $int).

% Premise 3: Security deposit >= monthly rent at managed buildings.
tff(premise_3, axiom,
    ! [B: building] : (managed_building(B) => $greatereq(security_deposit(B), monthly_rent(B)))).

% Premise 4: Fluffy is Tom's cat.
tff(premise_4a, axiom, cat(fluffy)).

% Premise 5: Cats are pets.
tff(premise_5, axiom,
    ! [A: animal] : (cat(A) => pet(A))).

% Premise 6: Olive Garden is managed.
tff(premise_6, axiom, managed_building(olive_garden)).

% Premise 7: Monthly rent at Olive Garden is $2000.
tff(premise_7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 9: Tom will rent if allowed to move in with Fluffy AND deposit <= $1500.
tff(premise_9, axiom,
    ! [B: building] :
      ((managed_building(B) & allowed_to_move_in_with(tom, fluffy, B) & $lesseq(security_deposit(B), 1500))
       => will_rent(tom, B))).

% Premise 10: If managed building allows pets, people can move in with a pet.
tff(premise_10, axiom,
    ! [P: person, A: animal, B: building] :
      ((managed_building(B) & allows_pets(B) & pet(A))
       => allowed_to_move_in_with(P, A, B))).

% Negated Conclusion: Tom will NOT rent at Olive Garden.
tff(goal, conjecture, ~will_rent(tom, olive_garden)).
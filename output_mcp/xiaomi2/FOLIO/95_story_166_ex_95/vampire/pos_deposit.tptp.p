tff(building_type, type, building: $tType).
tff(person_type, type, person: $tType).
tff(pet_type, type, pet: $tType).

tff(olive_garden_decl, type, olive_garden: building).
tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: pet).

tff(managed_building_decl, type, managed_building: building > $o).
tff(cat_decl, type, cat: pet > $o).
tff(is_pet_decl, type, is_pet: pet > $o).
tff(allowed_pets_in_decl, type, allowed_pets_in: building > $o).
tff(owns_decl, type, owns: (person * pet) > $o).
tff(allowed_move_in_decl, type, allowed_move_in_with_pet: (person * pet * building) > $o).
tff(will_rent_decl, type, will_rent: (person * building) > $o).
tff(deposit_required_decl, type, deposit_required: building > $o).
tff(monthly_rent_decl, type, monthly_rent: building > $int).
tff(security_deposit_decl, type, security_deposit: building > $int).

% Premise 1: Pets are allowed in some managed buildings.
tff(premise_1, axiom,
    ? [X: building] : (managed_building(X) & allowed_pets_in(X))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(premise_2, axiom,
    ! [X: building] : (managed_building(X) => deposit_required(X))).

% Premise 3: The security deposit is equal to the monthly rent or more at a managed building.
tff(premise_3, axiom,
    ! [X: building] : (managed_building(X) => $greatereq(security_deposit(X), monthly_rent(X)))).

% Premise 4: Fluffy is Tom's cat.
tff(premise_4a, axiom, cat(fluffy)).
tff(premise_4b, axiom, owns(tom, fluffy)).

% Premise 5: Cats are pets.
tff(premise_5, axiom,
    ! [X: pet] : (cat(X) => is_pet(X))).

% Premise 6: The Olive Garden is a managed building.
tff(premise_6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(premise_7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 8: $2000 is more than $1500.
tff(premise_8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent if allowed to move in with Fluffy and deposit <= $1500.
tff(premise_9, axiom,
    ! [X: building] :
      ((managed_building(X) & allowed_move_in_with_pet(tom, fluffy, X) & $lesseq(security_deposit(X), 1500))
       => will_rent(tom, X))).

% Premise 10: If a managed building allows pets, people can move in with a pet.
tff(premise_10, axiom,
    ! [X: building, P: person, Pt: pet] :
      ((managed_building(X) & allowed_pets_in(X))
       => allowed_move_in_with_pet(P, Pt, X))).

% Conclusion: The security deposit at the Olive Garden is $2000 or more.
tff(goal, conjecture, $greatereq(security_deposit(olive_garden), 2000)).
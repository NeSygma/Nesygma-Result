tff(person_type, type, person: $tType).
tff(animal_type, type, animal: $tType).
tff(building_type, type, building: $tType).

tff(tom_type, type, tom: person).
tff(fluffy_type, type, fluffy: animal).
tff(olive_garden_type, type, olive_garden: building).

tff(managed_type, type, managed: building > $o).
tff(allows_pets_type, type, allows_pets: building > $o).
tff(cat_type, type, cat: animal > $o).
tff(pet_type, type, pet: animal > $o).
tff(owns_type, type, owns: (person * animal) > $o).
tff(allowed_type, type, allowed_with_pet: (person * animal * building) > $o).
tff(deposit_req_type, type, deposit_req: building > $o).
tff(monthly_rent_type, type, monthly_rent: (building * $int) > $o).
tff(deposit_ge_type, type, deposit_ge: (building * $int) > $o).
tff(deposit_le_type, type, deposit_le: (person * building * $int) > $o).
tff(will_rent_type, type, will_rent: (person * building) > $o).

% Premise 1: Pets are allowed in some managed buildings
tff(p1, axiom, ? [B: building] : (managed(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent in a managed building
tff(p2, axiom, ! [B: building] : (managed(B) => deposit_req(B))).

% Premise 3: Security deposit >= monthly rent at managed buildings
tff(p3, axiom, ! [B: building, R: $int] :
    ((managed(B) & monthly_rent(B, R)) => deposit_ge(B, R))).

% Premise 3b: deposit_ge downward closure (if deposit >= A and A >= C, then deposit >= C)
tff(p3b, axiom, ! [B: building, A: $int, C: $int] :
    ((deposit_ge(B, A) & $greatereq(A, C)) => deposit_ge(B, C))).

% Premise 4: Fluffy is Tom's cat
tff(p4a, axiom, cat(fluffy)).
tff(p4b, axiom, owns(tom, fluffy)).

% Premise 5: Cats are pets
tff(p5, axiom, ! [A: animal] : (cat(A) => pet(A))).

% Premise 6: The Olive Garden is a managed building
tff(p6, axiom, managed(olive_garden)).

% Premise 7: Monthly rent at The Olive Garden is $2000
tff(p7, axiom, monthly_rent(olive_garden, 2000)).

% Premise 8: $2000 is more than $1500
tff(p8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent if allowed with Fluffy and deposit <= $1500
tff(p9, axiom, ! [B: building] :
    ((managed(B) & allowed_with_pet(tom, fluffy, B) & deposit_le(tom, B, 1500))
     => will_rent(tom, B))).

% Premise 10: If a managed building allows pets, people can move in with a pet
tff(p10, axiom, ! [B: building, P: person, A: animal] :
    ((managed(B) & allows_pets(B) & pet(A))
     => allowed_with_pet(P, A, B))).

% Connection: deposit >= high amount and high > low implies NOT deposit <= low
tff(deposit_conn, axiom, ! [B: building, P: person, H: $int, L: $int] :
    ((deposit_ge(B, H) & $greater(H, L))
     => ~deposit_le(P, B, L))).

% Conclusion: Tom is allowed to move into The Olive Garden with Fluffy
tff(conclusion, conjecture, allowed_with_pet(tom, fluffy, olive_garden)).
tff(entity_type, type, entity: $tType).
tff(fluffy_type, type, fluffy: entity).
tff(tom_type, type, tom: entity).
tff(olive_garden_type, type, olive_garden: entity).

tff(cat_type, type, cat: entity > $o).
tff(pet_type, type, pet: entity > $o).
tff(managed_building_type, type, managed_building: entity > $o).
tff(allows_pets_type, type, allows_pets: entity > $o).
tff(deposit_type, type, deposit: entity > $int).
tff(monthly_rent_type, type, monthly_rent: entity > $int).
tff(allowed_move_in_type, type, allowed_move_in: (entity * entity * entity) > $o).
tff(will_rent_type, type, will_rent: (entity * entity) > $o).

% Premise 1: Some managed buildings allow pets
fof(premise1, axiom, ? [B: entity] : (managed_building(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent in a managed building (deposit exists)
% Premise 3: Security deposit >= monthly rent at managed buildings
fof(premise3, axiom, ! [B: entity] : (managed_building(B) => $greatereq(deposit(B), monthly_rent(B)))).

% Premise 4: Fluffy is Tom's cat
fof(premise4a, axiom, cat(fluffy)).

% Premise 5: Cats are pets
fof(premise5, axiom, ! [X: entity] : (cat(X) => pet(X))).

% Premise 6: Olive Garden is a managed building
fof(premise6, axiom, managed_building(olive_garden)).

% Premise 7: Monthly rent at Olive Garden = $2000
fof(premise7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 8: $2000 > $1500 (used implicitly in reasoning)

% Premise 9: Tom will rent if allowed with Fluffy AND deposit <= $1500
fof(premise9, axiom, 
    (allowed_move_in(tom, fluffy, olive_garden) & $lesseq(deposit(olive_garden), 1500))
    => will_rent(tom, olive_garden)).

% Premise 10: If managed building allows pets, people allowed to move in with pet
fof(premise10, axiom, ! [B: entity, P: entity, Pet: entity] : 
    ((managed_building(B) & allows_pets(B) & pet(Pet)) 
     => allowed_move_in(P, Pet, B))).

% Conclusion: Security deposit at Olive Garden >= $2000
fof(goal, conjecture, $greatereq(deposit(olive_garden), 2000)).
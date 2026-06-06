% TFF: Tom will rent an apartment in The Olive Garden (positive)
tff(thing_type, type, thing: $tType).

tff(olive_garden_decl, type, olive_garden: thing).
tff(tom_decl, type, tom: thing).
tff(fluffy_decl, type, fluffy: thing).

tff(managed_building_type, type, managed_building: (thing) > $o).
tff(allows_pets_type, type, allows_pets: (thing) > $o).
tff(allowed_to_move_in_type, type, allowed_to_move_in: (thing * thing * thing) > $o).
tff(rent_apartment_type, type, rent_apartment: (thing * thing) > $o).
tff(security_deposit_type, type, security_deposit: (thing * $int) > $o).
tff(monthly_rent_func, type, monthly_rent: (thing) > $int).
tff(is_cat_type, type, is_cat: (thing) > $o).
tff(is_pet_type, type, is_pet: (thing) > $o).
tff(cat_of_type, type, cat_of: (thing * thing) > $o).

% Premise 1: Pets are allowed in some managed buildings.
tff(premise1, axiom, ? [B: thing] : (managed_building(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(premise2, axiom, ! [B: thing, P: thing] : (rent_apartment(P, B) => ? [D: $int] : security_deposit(B, D))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
tff(premise3, axiom, ! [B: thing, D: $int] : (security_deposit(B, D) => (D = monthly_rent(B) | $greatereq(D, monthly_rent(B))))).

% Premise 4: Fluffy is Tom's cat.
tff(premise4, axiom, is_cat(fluffy) & cat_of(fluffy, tom)).

% Premise 5: Cats are pets.
tff(premise5, axiom, ! [C: thing] : (is_cat(C) => is_pet(C))).

% Premise 6: The Olive Garden is a managed building.
tff(premise6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(premise7, axiom, monthly_rent(olive_garden) = 2000).

% Premise 8: $2000 is more than $1500.
tff(premise8, axiom, $greatereq(2000, 1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
tff(premise9, axiom, ! [B: thing, D: $int] : (managed_building(B) & security_deposit(B, D) & $lesseq(D, 1500) & allowed_to_move_in(tom, B, fluffy) => rent_apartment(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
tff(premise10, axiom, ! [B: thing, P: thing, Pet: thing] : (managed_building(B) & allows_pets(B) => allowed_to_move_in(P, B, Pet))).

% Additional fact: Fluffy is a pet (from premises 4 and 5).
tff(fluffy_is_pet, axiom, is_pet(fluffy)).

% Conclusion: Tom will rent an apartment in The Olive Garden.
tff(goal, conjecture, rent_apartment(tom, olive_garden)).
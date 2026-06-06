% Positive version: original claim as conjecture
% Using TFF with $int for arithmetic - properly typed

tff(managed_building_type, type, managed_building: $i > $o).
tff(allows_pets_type, type, allows_pets: $i > $o).
tff(deposit_required_type, type, deposit_required: $i > $o).
tff(security_deposit_at_least_rent_type, type, security_deposit_at_least_rent: $i > $o).
tff(cat_type, type, cat: $i > $o).
tff(pet_type, type, pet: $i > $o).
tff(monthly_rent_type, type, monthly_rent: ($i * $int) > $o).
tff(security_deposit_no_more_than_type, type, security_deposit_no_more_than: ($i * $int) > $o).
tff(allowed_move_in_with_pet_type, type, allowed_move_in_with_pet: ($i * $i) > $o).
tff(will_rent_type, type, will_rent: ($i * $i) > $o).

tff(distinct, axiom, (fluffy != tom & fluffy != olive_garden & tom != olive_garden)).

% Premise 1: Pets are allowed in some managed buildings.
tff(premise1, axiom, ? [B: $i] : (managed_building(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
tff(premise2, axiom, ! [B: $i] : (managed_building(B) => deposit_required(B))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
tff(premise3, axiom, ! [B: $i] : (managed_building(B) => security_deposit_at_least_rent(B))).

% Premise 4: Fluffy is Tom's cat.
tff(premise4, axiom, cat(fluffy)).

% Premise 5: Cats are pets.
tff(premise5, axiom, ! [X: $i] : (cat(X) => pet(X))).

% Premise 6: The Olive Garden is a managed building.
tff(premise6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
tff(premise7, axiom, monthly_rent(olive_garden, 2000)).

% Premise 8: $2000 is more than $1500.
tff(premise8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
tff(premise9, axiom, ! [B: $i] : ((managed_building(B) & allowed_move_in_with_pet(tom, B) & security_deposit_no_more_than(B, 1500)) => will_rent(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
tff(premise10, axiom, ! [B: $i, P: $i, Pet: $i] : ((managed_building(B) & allows_pets(B) & pet(Pet)) => allowed_move_in_with_pet(P, B))).

% Conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.
tff(goal, conjecture, allowed_move_in_with_pet(tom, olive_garden)).
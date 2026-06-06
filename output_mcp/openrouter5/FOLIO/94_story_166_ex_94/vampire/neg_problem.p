% Negative version: negated claim as conjecture

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

tff(premise1, axiom, ? [B: $i] : (managed_building(B) & allows_pets(B))).

tff(premise2, axiom, ! [B: $i] : (managed_building(B) => deposit_required(B))).

tff(premise3, axiom, ! [B: $i] : (managed_building(B) => security_deposit_at_least_rent(B))).

tff(premise4, axiom, cat(fluffy)).

tff(premise5, axiom, ! [X: $i] : (cat(X) => pet(X))).

tff(premise6, axiom, managed_building(olive_garden)).

tff(premise7, axiom, monthly_rent(olive_garden, 2000)).

tff(premise8, axiom, $greater(2000, 1500)).

tff(premise9, axiom, ! [B: $i] : ((managed_building(B) & allowed_move_in_with_pet(tom, B) & security_deposit_no_more_than(B, 1500)) => will_rent(tom, B))).

tff(premise10, axiom, ! [B: $i, P: $i, Pet: $i] : ((managed_building(B) & allows_pets(B) & pet(Pet)) => allowed_move_in_with_pet(P, B))).

% Negated conjecture: Tom is NOT allowed to move into an apartment in The Olive Garden with Fluffy.
tff(goal_neg, conjecture, ~allowed_move_in_with_pet(tom, olive_garden)).
% Using TFF with $int for arithmetic
tff(allows_pets_decl, type, allows_pets: $i > $o).
tff(deposit_required_decl, type, deposit_required: $i > $o).
tff(deposit_equal_rent_decl, type, deposit_equal_rent: $i > $o).
tff(deposit_more_than_rent_decl, type, deposit_more_than_rent: $i > $o).
tff(cat_decl, type, cat: $i > $o).
tff(pet_decl, type, pet: $i > $o).
tff(pet_owner_decl, type, pet_owner: ($i * $i) > $o).
tff(allowed_move_in_with_decl, type, allowed_move_in_with: ($i * $i * $i) > $o).
tff(will_rent_decl, type, will_rent: ($i * $i) > $o).
tff(security_deposit_no_more_than_decl, type, security_deposit_no_more_than: ($i * $int) > $o).
tff(monthly_rent_amount_decl, type, monthly_rent_amount: ($i * $int) > $o).
tff(deposit_amount_decl, type, deposit_amount: ($i * $int) > $o).
tff(more_than_decl, type, more_than: ($int * $int) > $o).
tff(managed_building_decl, type, managed_building: $i > $o).

tff(fluffy_decl, type, fluffy: $i).
tff(tom_decl, type, tom: $i).
tff(olive_garden_decl, type, olive_garden: $i).

% Pets are allowed in some managed buildings.
tff(pets_allowed_some, axiom, ? [B: $i] : (managed_building(B) & allows_pets(B))).

% A deposit is required to rent an apartment in a managed building.
tff(deposit_required_managed, axiom, ! [B: $i] : (managed_building(B) => deposit_required(B))).

% The security deposit can be either equal to the monthly rent at a managed building or more.
tff(deposit_equal_or_more, axiom, ! [B: $i] : (managed_building(B) => (deposit_equal_rent(B) | deposit_more_than_rent(B)))).

% Fluffy is Tom's cat.
tff(fluffy_is_cat, axiom, cat(fluffy)).
tff(fluffy_owner, axiom, pet_owner(tom, fluffy)).

% Cats are pets.
tff(cats_are_pets, axiom, ! [X: $i] : (cat(X) => pet(X))).

% The Olive Garden is a managed building.
tff(olive_garden_managed, axiom, managed_building(olive_garden)).

% The monthly rent at the Olive Garden is $2000.
tff(rent_olive_garden, axiom, monthly_rent_amount(olive_garden, 2000)).

% $2000 is more than $1500.
tff(more_than_2000_1500, axiom, more_than(2000, 1500)).

% Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
tff(tom_will_rent_condition, axiom, ! [B: $i] : ((managed_building(B) & allowed_move_in_with(tom, fluffy, B) & security_deposit_no_more_than(B, 1500)) => will_rent(tom, B))).

% If a managed building allows pets, then people are allowed to move in with a pet.
tff(allows_pets_implies_move_in, axiom, ! [B: $i] : ((managed_building(B) & allows_pets(B)) => ! [P: $i, A: $i] : ((pet_owner(P, A) & pet(A)) => allowed_move_in_with(P, A, B)))).

% If deposit equals rent and rent is R, then deposit amount is R.
tff(deposit_amount_relation, axiom, ! [B: $i, R: $int] : ((managed_building(B) & monthly_rent_amount(B, R) & deposit_equal_rent(B)) => deposit_amount(B, R))).

% If deposit is more than rent and rent is R, then deposit amount is some D > R.
tff(deposit_amount_relation2, axiom, ! [B: $i, R: $int] : ((managed_building(B) & monthly_rent_amount(B, R) & deposit_more_than_rent(B)) => ? [D: $int] : (deposit_amount(B, D) & more_than(D, R)))).

% If deposit amount is D and D is not more than 1500, then security deposit is no more than 1500.
tff(no_more_than_def, axiom, ! [B: $i, D: $int] : ((deposit_amount(B, D) & ~more_than(D, 1500)) => security_deposit_no_more_than(B, 1500))).

% If deposit amount is D and D is more than 1500, then security deposit is NOT no more than 1500.
tff(no_more_than_def2, axiom, ! [B: $i, D: $int] : ((deposit_amount(B, D) & more_than(D, 1500)) => ~security_deposit_no_more_than(B, 1500))).

% Conjecture: Tom will NOT rent an apartment in The Olive Garden.
tff(goal, conjecture, ~will_rent(tom, olive_garden)).
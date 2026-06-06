% TPTP file for the positive conjecture (TFF with $int arithmetic)
% Premises about pets, managed buildings, and Tom's situation

% Types

tff(tom_type, type, tom: $i).
tff(fluffy_type, type, fluffy: $i).
tff(olive_garden_type, type, olive_garden: $i).

tff(two_thousand_type, type, two_thousand: $int).
tff(fifteen_hundred_type, type, fifteen_hundred: $int).

% Predicates (all in tff for consistency)

tff(is_managed_building_decl, type, is_managed_building: $i > $o).
tff(allows_pets_decl, type, allows_pets: $i > $o).
tff(requires_deposit_decl, type, requires_deposit: $i > $o).
tff(is_cat_decl, type, is_cat: $i > $o).
tff(belongs_to_decl, type, belongs_to: ($i * $i) > $o).
tff(is_pet_decl, type, is_pet: $i > $o).
tff(monthly_rent_decl, type, monthly_rent: ($i * $int) > $o).
tff(security_deposit_decl, type, security_deposit: ($i * $int) > $o).
tff(allowed_to_move_in_with_pet_decl, type, allowed_to_move_in_with_pet: ($i * $i * $i) > $o).
tff(rents_decl, type, rents: ($i * $i) > $o).

% Facts

tff(is_managed_building_og, axiom, is_managed_building(olive_garden)).
tff(allows_pets_og, axiom, allows_pets(olive_garden)).
tff(requires_deposit_og, axiom, requires_deposit(olive_garden)).
tff(is_cat_fluffy, axiom, is_cat(fluffy)).
tff(belongs_to_fluffy_tom, axiom, belongs_to(fluffy, tom)).
tff(is_pet_fluffy, axiom, is_pet(fluffy)).
tff(monthly_rent_og, axiom, monthly_rent(olive_garden, two_thousand)).
tff(security_deposit_og, axiom, security_deposit(olive_garden, two_thousand)).

% Axioms

% 1. Pets are allowed in some managed buildings.

tff(some_managed_buildings_allow_pets, axiom, 
    ? [B: $i] : (is_managed_building(B) & allows_pets(B))).

% 2. A deposit is required to rent an apartment in a managed building.

tff(deposit_required, axiom, 
    ! [B: $i] : (is_managed_building(B) => requires_deposit(B))).

% 3. The security deposit can be either equal to the monthly rent at a managed building or more.

tff(deposit_ge_rent, axiom, 
    ! [B: $i, SD: $int, Rent: $int] : 
        ((is_managed_building(B) & security_deposit(B, SD) & monthly_rent(B, Rent)) 
         => $greatereq(SD, Rent))).

% 4. Fluffy is Tom's cat.

tff(fluffy_is_cat, axiom, is_cat(fluffy)).
tff(fluffy_belongs_to_tom, axiom, belongs_to(fluffy, tom)).

% 5. Cats are pets.

tff(cats_are_pets, axiom, 
    ! [C: $i] : (is_cat(C) => is_pet(C))).

% 6. The Olive Garden is a managed building.

tff(olive_garden_managed, axiom, is_managed_building(olive_garden)).

% 7. The monthly rent at the Olive Garden is $2000.

tff(olive_garden_rent, axiom, monthly_rent(olive_garden, two_thousand)).

% 8. $2000 is more than $1500.

tff(two_thousand_gt_fifteen_hundred, axiom, two_thousand > fifteen_hundred).

% 9. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.

tff(tom_rent_condition, axiom, 
    ! [B: $i, SD: $int] : 
        ((allowed_to_move_in_with_pet(tom, fluffy, B) & 
          security_deposit(B, SD) & $lesseq(SD, fifteen_hundred)) 
         => rents(tom, B))).

% 10. If a managed building allows pets, then people are allowed to move in with a pet.

tff(building_allows_pets_implies_allowed_with_pet, axiom, 
    ! [B: $i, P: $i, X: $i] : 
        ((is_managed_building(B) & allows_pets(B) & is_pet(X)) 
         => allowed_to_move_in_with_pet(P, X, B))).

% Conclusion to evaluate: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.

tff(conclusion, conjecture, allowed_to_move_in_with_pet(tom, fluffy, olive_garden)).
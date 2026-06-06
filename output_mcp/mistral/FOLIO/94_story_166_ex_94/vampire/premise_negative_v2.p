% TPTP file for the negated conjecture (corrected types)
% Premises about pets, managed buildings, and Tom's situation

% Define types (use $i for individuals, $int for integers)

% Constants (individuals)
fof(tom_decl, axiom, tom = tom).
fof(fluffy_decl, axiom, fluffy = fluffy).
fof(olive_garden_decl, axiom, olive_garden = olive_garden).

% Integer values for money
fof(two_thousand_decl, axiom, two_thousand = 2000).
fof(fifteen_hundred_decl, axiom, fifteen_hundred = 1500).

% Predicates
fof(is_managed_building_decl, axiom, is_managed_building(olive_garden)).
fof(allows_pets_decl, axiom, allows_pets(olive_garden)).
fof(requires_deposit_decl, axiom, requires_deposit(olive_garden)).
fof(is_cat_decl, axiom, is_cat(fluffy)).
fof(belongs_to_decl, axiom, belongs_to(fluffy, tom)).
fof(is_pet_decl, axiom, is_pet(fluffy)).
fof(monthly_rent_decl, axiom, monthly_rent(olive_garden) = two_thousand).
fof(security_deposit_decl, axiom, security_deposit(olive_garden) = two_thousand).

% Axioms

% 1. Pets are allowed in some managed buildings.
fof(some_managed_buildings_allow_pets, axiom, 
    ? [B] : (is_managed_building(B) & allows_pets(B))).

% 2. A deposit is required to rent an apartment in a managed building.
fof(deposit_required, axiom, 
    ! [B] : (is_managed_building(B) => requires_deposit(B))).

% 3. The security deposit can be either equal to the monthly rent at a managed building or more.
fof(deposit_ge_rent, axiom, 
    ! [B] : (is_managed_building(B) => 
        $greatereq(security_deposit(B), monthly_rent(B)))).

% 4. Fluffy is Tom's cat.
fof(fluffy_is_cat, axiom, is_cat(fluffy)).
fof(fluffy_belongs_to_tom, axiom, belongs_to(fluffy, tom)).

% 5. Cats are pets.
fof(cats_are_pets, axiom, 
    ! [C] : (is_cat(C) => is_pet(C))).

% 6. The Olive Garden is a managed building.
fof(olive_garden_managed, axiom, is_managed_building(olive_garden)).

% 7. The monthly rent at the Olive Garden is $2000.
fof(olive_garden_rent, axiom, monthly_rent(olive_garden) = two_thousand).

% 8. $2000 is more than $1500.
fof(two_thousand_gt_fifteen_hundred, axiom, two_thousand > fifteen_hundred).

% 9. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
fof(tom_rent_condition, axiom, 
    ! [B] : ((allowed_to_move_in_with_pet(tom, fluffy, B) & 
                          $lesseq(security_deposit(B), fifteen_hundred)) 
                         => rents(tom, B))).

% 10. If a managed building allows pets, then people are allowed to move in with a pet.
fof(building_allows_pets_implies_allowed_with_pet, axiom, 
    ! [B, P, X] : ((is_managed_building(B) & allows_pets(B) & is_pet(X)) 
         => allowed_to_move_in_with_pet(P, X, B))).

% Negated conclusion: Tom is NOT allowed to move into an apartment in The Olive Garden with Fluffy.
fof(conclusion_negation, conjecture, ~allowed_to_move_in_with_pet(tom, fluffy, olive_garden)).
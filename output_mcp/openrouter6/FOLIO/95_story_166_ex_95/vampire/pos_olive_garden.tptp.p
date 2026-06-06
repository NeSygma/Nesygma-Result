% Types
tff(building_type, type, building: $tType).
tff(person_type, type, person: $tType).
tff(pet_type, type, pet: $tType).

% Constants
tff(olive_garden_decl, type, olive_garden: building).
tff(tom_decl, type, tom: person).
tff(fluffy_decl, type, fluffy: pet).

% Predicates
tff(managed_building_decl, type, managed_building: (building) > $o).
tff(allows_pets_decl, type, allows_pets: (building) > $o).
tff(deposit_required_decl, type, deposit_required: (building) > $o).
tff(security_deposit_decl, type, security_deposit: (building * $int) > $o).
tff(monthly_rent_decl, type, monthly_rent: (building * $int) > $o).
tff(cat_decl, type, cat: (pet) > $o).
tff(pet_decl, type, pet: (pet) > $o).
tff(owns_decl, type, owns: (person * pet) > $o).
tff(can_move_in_with_decl, type, can_move_in_with: (person * pet * building) > $o).
tff(rent_apartment_decl, type, rent_apartment: (person * building) > $o).

% Axioms
tff(pets_allowed_some, axiom, ? [X: building] : (managed_building(X) & allows_pets(X))).
tff(deposit_required_all, axiom, ! [X: building] : (managed_building(X) => deposit_required(X))).
tff(security_deposit_rule, axiom, ! [X: building, D: $int, R: $int] : 
    (managed_building(X) & security_deposit(X, D) & monthly_rent(X, R) => (D = R | $greater(D, R)))).
tff(fluffy_is_cat, axiom, cat(fluffy)).
tff(tom_owns_fluffy, axiom, owns(tom, fluffy)).
tff(cats_are_pets, axiom, ! [P: pet] : (cat(P) => pet(P))).
tff(olive_garden_managed, axiom, managed_building(olive_garden)).
tff(olive_garden_rent, axiom, monthly_rent(olive_garden, 2000)).
tff(two_thousand_more, axiom, $greater(2000, 1500)).
tff(tom_rent_condition, axiom, 
    ! [X: building] : 
        (managed_building(X) & can_move_in_with(tom, fluffy, X) & 
         ? [D: $int] : (security_deposit(X, D) & $lesseq(D, 1500))
         => rent_apartment(tom, X))).
tff(allow_pets_implies_move_in, axiom,
    ! [X: building, P: person, Pet: pet] :
        (managed_building(X) & allows_pets(X) & pet(Pet) => can_move_in_with(P, Pet, X))).
tff(security_deposit_exists, axiom, ! [X: building] : (managed_building(X) => ? [D: $int] : security_deposit(X, D))).

% Conjecture: security deposit at Olive Garden is $2000 or more
tff(goal, conjecture, ! [D: $int] : (security_deposit(olive_garden, D) => (D = 2000 | $greater(D, 2000)))).
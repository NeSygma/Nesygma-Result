% TPTP problem for Olive Garden security deposit evaluation (negated)
% Using relational modeling to avoid type issues

fof(managed_building_type, axiom, managed_building(olive_garden)).
fof(pet_type, axiom, pet(fluffy)).
fof(cat_type, axiom, cat(fluffy)).
fof(tom_has_cat, axiom, tom_has_cat(fluffy)).

% Amounts as constants
fof(amount_2000, axiom, amount_2000).
fof(amount_1500, axiom, amount_1500).

% Greater than relation
fof(greater_2000_1500, axiom, greater(2000, 1500)).

% Rent at Olive Garden is $2000
fof(rent_olive_garden, axiom, rent(olive_garden, 2000)).

% Premise: Pets are allowed in some managed buildings
fof(pets_allowed_some, axiom, ? [X] : (managed_building(X) & allows_pets(X))).

% Premise: Deposit required for managed buildings
fof(deposit_required_all, axiom, ! [X] : (managed_building(X) => deposit_required(X))).

% Premise: Security deposit ≥ monthly rent
fof(deposit_ge_rent, axiom, ! [X, A, B] : 
    ((managed_building(X) & rent(X, B) & deposit(X, A)) => greater(A, B) | A = B)).

% Premise: Cats are pets
fof(cats_are_pets, axiom, ! [C] : (cat(C) => pet(C))).

% Premise: Tom will rent if allowed to move in with Fluffy AND deposit ≤ $1500
fof(tom_will_rent_condition, axiom, 
    ! [X] : (tom_will_rent(X) <=> 
        (allows_move_in(X, fluffy) & deposit(X, A) & ~greater(A, 1500)))).

% Premise: If building allows pets, then people can move in with pets
fof(allows_pets_implies_move_in, axiom, 
    ! [X, P] : (allows_pets(X) => allows_move_in(X, P))).

% NEGATED Conclusion: Security deposit at Olive Garden is NOT (either $2000 or more)
% This means: deposit < $2000 (strictly less than 2000)
fof(goal_negated, conjecture, ? [A] : (deposit(olive_garden, A) & greater(2000, A))).
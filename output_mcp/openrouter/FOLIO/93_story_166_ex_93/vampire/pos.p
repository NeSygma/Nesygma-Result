% Entities
fof(distinct_entities, axiom, (tom != fluffy & tom != olive_garden & fluffy != olive_garden & val2000 != val1500)).

% Managed building
fof(olive_garden_managed, axiom, managed_building(olive_garden)).

% Some managed building allows pets
fof(some_allows_pets, axiom, ? [B] : (managed_building(B) & allows_pets(B))).

% Security deposit relation
fof(security_deposit_rule, axiom,
    ! [B,R,D] : (monthly_rent(B,R) & security_deposit(B,D) => (equal(D,R) | more_than(D,R)))).

% Monthly rent
fof(rent_olive, axiom, monthly_rent(olive_garden, val2000)).

% More than fact
fof(more_2000_1500, axiom, more_than(val2000, val1500)).

% Cats are pets
fof(cat_pet, axiom, ! [X] : (cat(X) => pet(X))).

% Fluffy is Tom's cat
fof(fluffy_cat, axiom, cat(fluffy)).

% Rule: if a managed building allows pets then people are allowed to move in with a pet
fof(pet_move_rule, axiom,
    ! [B,P,Person] : (managed_building(B) & allows_pets(B) & pet(P) => allowed_move(Person,P))).

% Existence of security deposit for olive garden
fof(exist_deposit_olive, axiom, ? [D] : security_deposit(olive_garden, D)).

% Rule for renting
fof(rent_rule, axiom,
    ! [Person,Building,Pet,DepAmt] : ((allowed_move(Person,Pet) & security_deposit(Building,DepAmt) & ~more_than(DepAmt, val1500) & managed_building(Building)) => rent(Person,Building))).

% Conjecture
fof(goal, conjecture, rent(tom, olive_garden)).
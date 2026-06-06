% Negative version: negated conclusion as conjecture
% Negated conclusion: It is NOT the case that the security deposit at the Olive Garden is either $2000 or more.
% i.e., For all D, if security_deposit(olive_garden, D) then D < 2000.

tff(managed_building_type, type, managed_building: $tType).
tff(pet_type, type, pet: $tType).
tff(person_type, type, person: $tType).

% Constants
tff(olive_garden_decl, type, olive_garden: managed_building).
tff(fluffy_decl, type, fluffy: pet).
tff(tom_decl, type, tom: person).

% Predicates
tff(pets_allowed_decl, type, pets_allowed: managed_building > $o).
tff(deposit_required_decl, type, deposit_required: managed_building > $o).
tff(security_deposit_decl, type, security_deposit: (managed_building * $int) > $o).
tff(monthly_rent_decl, type, monthly_rent: (managed_building * $int) > $o).
tff(cat_decl, type, cat: pet > $o).
tff(pet_decl, type, pet: pet > $o).
tff(owns_decl, type, owns: (person * pet) > $o).
tff(allowed_move_in_decl, type, allowed_move_in: (person * pet * managed_building) > $o).
tff(will_rent_decl, type, will_rent: (person * managed_building) > $o).

% Premise 1: Pets are allowed in some managed buildings.
fof(premise1, axiom, ? [B: managed_building] : pets_allowed(B)).

% Premise 2: A deposit is required to rent an apartment in a managed building.
fof(premise2, axiom, ! [B: managed_building] : deposit_required(B)).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
fof(premise3, axiom, ! [B: managed_building, R: $int] : 
    (monthly_rent(B, R) => ? [D: $int] : (security_deposit(B, D) & $greatereq(D, R)))).

% Premise 4: Fluffy is Tom's cat.
fof(premise4, axiom, cat(fluffy)).
fof(premise4b, axiom, owns(tom, fluffy)).

% Premise 5: Cats are pets.
fof(premise5, axiom, ! [P: pet] : (cat(P) => pet(P))).

% Premise 7: The monthly rent at the Olive Garden is $2000.
fof(premise7, axiom, monthly_rent(olive_garden, 2000)).

% Premise 8: $2000 is more than $1500.
fof(premise8, axiom, $greater(2000, 1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
fof(premise9, axiom, ! [B: managed_building, D: $int] : 
    ((allowed_move_in(tom, fluffy, B) & security_deposit(B, D) & $lesseq(D, 1500)) => will_rent(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
fof(premise10, axiom, ! [B: managed_building, P: pet, Person: person] : 
    ((pets_allowed(B) & pet(P) & owns(Person, P)) => allowed_move_in(Person, P, B))).

% Negated conclusion: It is NOT the case that the security deposit at the Olive Garden is $2000 or more.
% i.e., For all D, if security_deposit(olive_garden, D) then D < 2000.
fof(neg_conclusion, conjecture, ! [D: $int] : (security_deposit(olive_garden, D) => $less(D, 2000))).
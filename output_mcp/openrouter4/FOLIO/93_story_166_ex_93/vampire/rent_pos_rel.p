% Relational FOF encoding without arithmetic types
% Use constants for amounts and predicates for comparisons

% Predicates
fof(managed_building_decl, predicate, managed_building(B)).
fof(allows_pets_decl, predicate, allows_pets(B)).
fof(deposit_required_decl, predicate, deposit_required(B)).
fof(cat_decl, predicate, cat(X)).
fof(pet_decl, predicate, pet(X)).
fof(owns_decl, predicate, owns(P, X)).
fof(allowed_move_in_with_decl, predicate, allowed_move_in_with(P, X, B)).
fof(tom_rents_decl, predicate, tom_rents(P, B)).
fof(monthly_rent_is_decl, predicate, monthly_rent_is(B, A)).
fof(security_deposit_is_decl, predicate, security_deposit_is(B, A)).
fof(greater_decl, predicate, greater(A1, A2)).
fof(lesseq_decl, predicate, lesseq(A1, A2)).
fof(eq_amount_decl, predicate, eq_amount(A1, A2)).

% Constants for amounts
fof(amt_2000_decl, predicate, amount(amt_2000)).
fof(amt_1500_decl, predicate, amount(amt_1500)).

% Distinct amounts
fof(distinct_amounts, axiom, amt_2000 != amt_1500).

% Premise 1: Pets are allowed in some managed buildings.
fof(p1, axiom, ? [B] : (managed_building(B) & allows_pets(B))).

% Premise 2: A deposit is required to rent an apartment in a managed building.
fof(p2, axiom, ! [B] : (managed_building(B) => deposit_required(B))).

% Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more.
fof(p3, axiom, ! [B, R, D] : ((managed_building(B) & monthly_rent_is(B, R) & security_deposit_is(B, D)) => (eq_amount(D, R) | greater(D, R)))).

% Premise 4: Fluffy is Tom's cat.
fof(p4, axiom, (cat(fluffy) & owns(tom, fluffy))).

% Premise 5: Cats are pets.
fof(p5, axiom, ! [X] : (cat(X) => pet(X))).

% Premise 6: The Olive Garden is a managed building.
fof(p6, axiom, managed_building(olive_garden)).

% Premise 7: The monthly rent at the Olive Garden is $2000.
fof(p7, axiom, monthly_rent_is(olive_garden, amt_2000)).

% Premise 8: $2000 is more than $1500.
fof(p8, axiom, greater(amt_2000, amt_1500)).

% Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
fof(p9, axiom, ! [B, D] : ((managed_building(B) & allowed_move_in_with(tom, fluffy, B) & security_deposit_is(B, D) & lesseq(D, amt_1500)) => tom_rents(tom, B))).

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
fof(p10, axiom, ! [B] : ((managed_building(B) & allows_pets(B)) => ! [P, X] : (pet(X) => allowed_move_in_with(P, X, B)))).

% Conclusion: Tom will rent an apartment in The Olive Garden.
fof(goal, conjecture, tom_rents(tom, olive_garden)).
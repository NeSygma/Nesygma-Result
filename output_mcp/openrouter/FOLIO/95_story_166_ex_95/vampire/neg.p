% Negative TPTP
% Types
tff(managed_type, type, managed: $i > $o).
 tff(allows_pets_type, type, allows_pets: $i > $o).
 tff(deposit_type, type, deposit: ($i * $int) > $o).
 tff(monthly_rent_type, type, monthly_rent: ($i * $int) > $o).
 tff(cat_type, type, cat: $i > $o).
 tff(pet_type, type, pet: $i > $o).
 tff(allowed_move_in_with_type, type, allowed_move_in_with: ($i * $i) > $o).
 tff(tom_type, type, tom: $i).
 tff(fluffy_type, type, fluffy: $i).
 tff(olive_garden_type, type, olive_garden: $i).

% Axioms (same as positive)
 tff(pets_allowed_some, axiom, ? [B: $i] : (managed(B) & allows_pets(B))).
 tff(deposit_exists, axiom, ! [B: $i] : (managed(B) => ? [D: $int] : deposit(B,D))).
 tff(deposit_relation, axiom, ! [B: $i, R: $int, D: $int] : ((managed(B) & monthly_rent(B,R) & deposit(B,D)) => (D = R | $greater(D,R)))).
 tff(cat_pet, axiom, ! [X: $i] : (cat(X) => pet(X))).
 tff(fluffy_cat, axiom, cat(fluffy)).
 tff(olive_managed, axiom, managed(olive_garden)).
 tff(olive_rent, axiom, monthly_rent(olive_garden,2000)).
 tff(more_2000_1500, axiom, $greater(2000,1500)).
 tff(pet_move_allowed, axiom, ! [B: $i] : ((managed(B) & allows_pets(B)) => allowed_move_in_with(tom,fluffy))).

% Negated goal: No deposit at Olive Garden is $2000 or more.
 tff(neg_goal, conjecture, ! [D: $int] : ~(deposit(olive_garden,D) & $greatereq(D,2000))).
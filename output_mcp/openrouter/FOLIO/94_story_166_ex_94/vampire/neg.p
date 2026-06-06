% Negative version
fof(cat_fluffy, axiom, cat(fluffy)).
fof(pet_of_cat, axiom, ! [X] : (cat(X) => pet(X))).
fof(fluffy_owned_by_tom, axiom, owned_by(fluffy, tom)).
fof(managed_olive, axiom, managed_building(olive_garden)).
fof(pets_allowed_some, axiom, ? [B] : (managed_building(B) & allows_pets(B))).
fof(rule_allowed_move, axiom, ! [B,P,Pet] : ((managed_building(B) & allows_pets(B) & pet(Pet) & owned_by(Pet,P)) => allowed_move_in_with(P,Pet,B))).
fof(distinct, axiom, (tom != fluffy & tom != olive_garden & fluffy != olive_garden)).
fof(goal, conjecture, ~allowed_move_in_with(tom,fluffy,olive_garden)).
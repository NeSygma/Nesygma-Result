% Positive file: Is Tom allowed to move into The Olive Garden with Fluffy?
fof(premise_1, axiom, ? [X] : (managed_building(X) & pets_allowed_in(X))).
fof(premise_4, axiom, cat(fluffy)).
fof(premise_5, axiom, ! [X] : (cat(X) => pet(X))).
fof(premise_6, axiom, managed_building(the_olive_garden)).
fof(premise_10, axiom, ! [X] : ((managed_building(X) & pets_allowed_in(X)) => ! [P, A] : (pet(A) => allowed_move_in_with(P, X, A)))).
fof(distinct, axiom, (fluffy != tom & fluffy != the_olive_garden & tom != the_olive_garden)).
fof(conclusion, conjecture, allowed_move_in_with(tom, the_olive_garden, fluffy)).
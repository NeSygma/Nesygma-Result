fof(premise_1, axiom, ? [X] : (managed(X) & pets_allowed(X))).
fof(premise_2, axiom, ! [X] : (managed(X) => deposit_req(X))).
fof(deposit_exists, axiom, ! [X] : (deposit_req(X) => ? [D] : deposit_amt(X, D))).
fof(premise_3, axiom, ! [X, D, R] : ((managed(X) & deposit_amt(X, D) & rent_amt(X, R)) => (D = R | more(D, R)))).
fof(premise_4, axiom, cat(fluffy)).
fof(premise_5, axiom, ! [X] : (cat(X) => pet(X))).
fof(premise_6, axiom, managed(olive_garden)).
fof(premise_7, axiom, rent_amt(olive_garden, a2000)).
fof(premise_8, axiom, more(a2000, a1500)).
fof(premise_9, axiom, ! [X, D] : ((managed(X) & can_move_in(tom, fluffy, X) & deposit_amt(X, D) & ~more(D, a1500)) => will_rent(tom, X))).
fof(premise_10, axiom, ! [X, P, A] : ((managed(X) & pets_allowed(X) & person(P) & pet(A)) => can_move_in(P, A, X))).
fof(person_tom, axiom, person(tom)).
fof(distinct_constants, axiom, (olive_garden != fluffy & olive_garden != tom & olive_garden != a2000 & olive_garden != a1500 & fluffy != tom & fluffy != a2000 & fluffy != a1500 & tom != a2000 & tom != a1500 & a2000 != a1500)).
fof(neg_conclusion, conjecture, ! [D] : (deposit_amt(olive_garden, D) => (D != a2000 & ~more(D, a2000)))).
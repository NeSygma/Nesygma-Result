fof(premise_1, axiom, ? [B] : (managed_building(B) & allows_pets(B))).
fof(premise_2, axiom, ! [B] : (managed_building(B) => deposit_required(B))).
fof(premise_3, axiom, ! [B,R,D] : ((managed_building(B) & monthly_rent(B,R) & deposit_amount(B,D)) => (deposit_equals(D,R) | more_than(D,R)))).
fof(premise_4, axiom, cat(fluffy)).
fof(premise_5, axiom, owner(tom, fluffy)).
fof(premise_6, axiom, ! [X] : (cat(X) => pet(X))).
fof(premise_7, axiom, managed_building(olive_garden)).
fof(premise_8, axiom, monthly_rent(olive_garden, amount_2000)).
fof(premise_9, axiom, more_than(amount_2000, amount_1500)).
fof(premise_10, axiom, ! [P,B,Pet] : ((allowed_to_move_in(P,B,Pet) & owner(P,Pet) & deposit_within_limit(B,amount_1500)) => will_rent(P,B))).
fof(premise_11, axiom, ! [B,P,Pet] : ((managed_building(B) & allows_pets(B) & pet(Pet)) => allowed_to_move_in(P,B,Pet))).
fof(premise_12, axiom, ! [B,D] : (deposit_within_limit(B,D) <=> ? [D2] : (deposit_amount(B,D2) & (deposit_equals(D2,D) | less_than(D2,D))))).
fof(premise_13, axiom, ! [X,Y] : (more_than(X,Y) => ~less_than(X,Y))).
fof(premise_14, axiom, ! [X,Y] : (more_than(X,Y) => ~deposit_equals(X,Y))).
fof(premise_15, axiom, ! [X,Y] : (deposit_equals(X,Y) => ~less_than(X,Y))).
fof(premise_16, axiom, ! [B] : (managed_building(B) => ? [D] : deposit_amount(B,D))).
fof(premise_17, axiom, ! [B,D1,D2] : ((deposit_amount(B,D1) & deposit_amount(B,D2)) => D1 = D2)).
fof(goal, conjecture, allowed_to_move_in(tom, olive_garden, fluffy)).
% Negative version (negated claim)
fof(cove_barutin, axiom, cove(barutin_cove)).
fof(named_barutin, axiom, named_after(barutin_cove, barutin_settlement)).
fof(bulgaria_barutin, axiom, bulgaria_place(barutin_settlement)).
fof(loc_barutin_snow, axiom, located_in(barutin_cove, snow_island)).
fof(loc_snow_south, axiom, located_in(snow_island, south_chetland_islands)).
fof(loc_antarctica_south, axiom, located_in(antarctica, south_chetland_islands)).
fof(transitivity, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(goal_neg, conjecture, ! [X,Y] : ~ (cove(X) & named_after(X,Y) & bulgaria_place(Y) & located_in(X, antarctica))).
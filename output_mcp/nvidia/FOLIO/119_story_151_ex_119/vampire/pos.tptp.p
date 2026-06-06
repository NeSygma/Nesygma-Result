fof(axiom_cove, axiom, cove(barutin_cove)).
fof(axiom_named_after, axiom, named_after(barutin_cove, barutin_settlement)).
fof(axiom_bulgarian, axiom, bulgarian(barutin_settlement)).
fof(axiom_loc1, axiom, located_in(barutin_cove, snow_island)).
fof(axiom_loc2, axiom, located_in(snow_island, south_shetland_islands)).
fof(axiom_loc3, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(axiom_loc4, axiom, located_in(deception_island, south_shetland_islands)).
fof(axiom_loc5, axiom, located_in(antarctica, south_shetland_islands)).
fof(trans, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(conclusion, conjecture, ? [X] : (cove(X) & located_in(X, antarctica) & ? [Y] : (named_after(X,Y) & bulgarian(Y)))).
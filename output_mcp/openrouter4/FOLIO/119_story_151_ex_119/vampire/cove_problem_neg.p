fof(premise1a, axiom, cove(barutin_cove)).
fof(premise1b, axiom, named_after_bulgarian_place(barutin_cove)).
fof(premise2, axiom, located_in(barutin_cove, snow_island)).
fof(premise3_snow, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise3_greenwich, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise3_deception, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise4, axiom, located_in(antarctica, south_shetland_islands)).
fof(premise5, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(distinct, axiom, (barutin_cove != antarctica & barutin_cove != snow_island & barutin_cove != south_shetland_islands & snow_island != antarctica & snow_island != south_shetland_islands & antarctica != south_shetland_islands)).
fof(neg_conclusion, conjecture, ~? [X] : (cove(X) & located_in(X, antarctica) & named_after_bulgarian_place(X))).
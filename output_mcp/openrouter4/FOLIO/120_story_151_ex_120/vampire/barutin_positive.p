fof(distinct, axiom, (barutin_cove != snow_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & snow_island != south_shetland_islands & snow_island != antarctica & south_shetland_islands != antarctica)).
fof(fact1, axiom, located_in(barutin_cove, snow_island)).
fof(fact2, axiom, located_in(snow_island, south_shetland_islands)).
fof(fact3, axiom, located_in(south_shetland_islands, antarctica)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(goal, conjecture, ~located_in(barutin_cove, antarctica)).
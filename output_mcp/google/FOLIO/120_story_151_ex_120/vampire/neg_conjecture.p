fof(barutin_cove_in_antarctica, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_in_ssi, axiom, located_in(snow_island, south_shetland_islands)).
fof(antarctica_in_ssi, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(distinct, axiom, (barutin_cove != snow_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & snow_island != south_shetland_islands & snow_island != antarctica & south_shetland_islands != antarctica)).
fof(goal, conjecture, located_in(barutin_cove, antarctica)).
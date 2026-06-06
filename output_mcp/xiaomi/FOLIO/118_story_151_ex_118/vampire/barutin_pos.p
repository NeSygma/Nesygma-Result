fof(named_after_fact, axiom, named_after(barutin_cove, barutin)).
fof(cove_fact, axiom, cove(barutin_cove)).
fof(located_in_1, axiom, located_in(barutin_cove, snow_island)).
fof(located_in_2, axiom, located_in(snow_island, south_shetland_islands)).
fof(located_in_3, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(located_in_4, axiom, located_in(deception_island, south_shetland_islands)).
fof(located_in_5, axiom, located_in(antarctica, south_shetland_islands)).
fof(island_1, axiom, island(snow_island)).
fof(island_2, axiom, island(greenwich_island)).
fof(island_3, axiom, island(deception_island)).
fof(transitivity, axiom, ! [X, Y, Z] : ((located_in(X, Y) & located_in(Y, Z)) => located_in(X, Z))).
fof(goal, conjecture, ! [X] : ((island(X) & located_in(X, antarctica)) => named_after(barutin_cove, X))).
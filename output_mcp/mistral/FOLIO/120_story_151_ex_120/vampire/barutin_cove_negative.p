fof(barutin_cove_snow_island, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(south_shetland_antarctica, axiom, located_in(south_shetland_islands, antarctica)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(conclusion, conjecture, located_in(barutin_cove, antarctica)).
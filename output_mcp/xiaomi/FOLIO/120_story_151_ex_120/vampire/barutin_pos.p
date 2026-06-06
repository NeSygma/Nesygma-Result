fof(barutin_is_cove, axiom, cove(barutin_cove)).
fof(barutin_named, axiom, named_after(barutin_cove, barutin)).
fof(barutin_on_snow, axiom, located_in(barutin_cove, snow_island)).
fof(snow_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_in_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_in_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_in_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(goal, conjecture, ~located_in(barutin_cove, antarctica)).
fof(named_after_barutin_cove, axiom, named_after(barutin_cove, barutin_settlement)).
fof(is_a_cove_barutin_cove, axiom, is_a_cove(barutin_cove)).
fof(is_a_settlement_barutin_settlement, axiom, is_a_settlement(barutin_settlement)).
fof(barutin_cove_on_southwest_coast, axiom, located_in(barutin_cove, southwest_coast_snow_island)).
fof(southwest_coast_on_snow_island, axiom, located_in(southwest_coast_snow_island, snow_island)).
fof(is_a_coast_southwest_coast, axiom, is_a_coast(southwest_coast_snow_island)).
fof(snow_island_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_in_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_in_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_in_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity_located_in, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(conclusion, conjecture, ~located_in(barutin_cove, antarctica)).
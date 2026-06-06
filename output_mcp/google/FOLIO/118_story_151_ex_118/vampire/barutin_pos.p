fof(barutin_cove_named_after_barutin, axiom, named_after(barutin_cove, barutin_settlement)).
fof(barutin_cove_location, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_location, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_location, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_location, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_location, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(is_island_def, axiom, (is_island(snow_island) & is_island(greenwich_island) & is_island(deception_island))).
fof(distinct_entities, axiom, (barutin_cove != barutin_settlement & barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & barutin_settlement != snow_island & barutin_settlement != greenwich_island & barutin_settlement != deception_island & barutin_settlement != south_shetland_islands & barutin_settlement != antarctica & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & greenwich_island != deception_island & greenwich_island != south_shetland_islands & greenwich_island != antarctica & deception_island != south_shetland_islands & deception_island != antarctica & south_shetland_islands != antarctica)).
fof(conclusion, conjecture, ! [I] : ((is_island(I) & located_in(I, antarctica)) => named_after(barutin_cove, I))).
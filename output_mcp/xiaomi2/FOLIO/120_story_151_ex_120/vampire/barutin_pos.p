fof(barutin_in_snow, axiom, located_in(barutin_cove, snow_island)).
fof(snow_in_ssi, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_in_ssi, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_in_ssi, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_in_ssi, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(distinct_entities, axiom, (barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & greenwich_island != deception_island & greenwich_island != south_shetland_islands & greenwich_island != antarctica & deception_island != south_shetland_islands & deception_island != antarctica & south_shetland_islands != antarctica)).
fof(goal, conjecture, ~located_in(barutin_cove, antarctica)).
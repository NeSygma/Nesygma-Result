fof(island_snow, axiom, island(snow_island)).
fof(island_greenwich, axiom, island(greenwich_island)).
fof(island_deception, axiom, island(deception_island)).
fof(located_snow, axiom, located_in(snow_island, south_shetland_islands)).
fof(located_greenwich, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(located_deception, axiom, located_in(deception_island, south_shetland_islands)).
fof(located_antarctica, axiom, located_in(antarctica, south_shetland_islands)).
fof(located_barutin_cove, axiom, located_in(barutin_cove, snow_island)).
fof(named_barutin_cove, axiom, named_after(barutin_cove, barutin_settlement)).
fof(transitivity, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(distinctness, axiom, (barutin_cove != barutin_settlement & barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & barutin_settlement != snow_island & barutin_settlement != greenwich_island & barutin_settlement != deception_island & barutin_settlement != south_shetland_islands & barutin_settlement != antarctica & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & greenwich_island != deception_island & greenwich_island != south_shetland_islands & greenwich_island != antarctica & deception_island != south_shetland_islands & deception_island != antarctica & south_shetland_islands != antarctica)).
fof(conjecture, conjecture, ? [X] : (island(X) & located_in(X, antarctica) & ~named_after(barutin_cove, X))).
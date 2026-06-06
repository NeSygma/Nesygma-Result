fof(barutin_cove_is_cove, axiom, cove(barutin_cove)).
fof(barutin_settlement_is_settlement, axiom, settlement(barutin_settlement)).
fof(named_after_barutin_cove, axiom, named_after(barutin_cove, barutin_settlement)).
fof(barutin_cove_located_in_snow_island, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_is_island, axiom, island(snow_island)).
fof(greenwich_island_is_island, axiom, island(greenwich_island)).
fof(deception_island_is_island, axiom, island(deception_island)).
fof(south_shetland_islands_place, axiom, place(south_shetland_islands)).
fof(antarctica_is_continent, axiom, continent(antarctica)).
fof(snow_island_located_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_located_in_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_located_in_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_located_in_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(place_definitions, axiom, place(barutin_cove) & place(barutin_settlement) & place(snow_island) & place(greenwich_island) & place(deception_island) & place(south_shetland_islands) & place(antarctica)).
fof(distinct_places, axiom, barutin_cove != barutin_settlement & barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & barutin_settlement != snow_island & barutin_settlement != greenwich_island & barutin_settlement != deception_island & barutin_settlement != south_shetland_islands & barutin_settlement != antarctica & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & greenwich_island != deception_island & greenwich_island != south_shetland_islands & greenwich_island != antarctica & deception_island != south_shetland_islands & deception_island != antarctica & south_shetland_islands != antarctica).
fof(island_in_antarctica_def, axiom, ! [X] : (island_in_antarctica(X) <=> (island(X) & located_in(X, antarctica)))).
fof(conclusion, conjecture, ! [X] : (island_in_antarctica(X) => named_after(barutin_cove, X))).
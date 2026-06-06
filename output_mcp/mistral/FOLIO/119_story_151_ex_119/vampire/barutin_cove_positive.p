fof(barutin_cove_named_after, axiom, named_after(barutin_cove, barutin_settlement)).
fof(barutin_settlement_in_bulgaria, axiom, located_in(barutin_settlement, bulgaria)).
fof(barutin_cove_in_snow_island, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_in_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_in_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(antarctica_in_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).
fof(location_transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(barutin_cove_is_cove, axiom, is_cove(barutin_cove)).
fof(distinct_places, axiom, (barutin_cove != barutin_settlement & barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & barutin_cove != bulgaria & barutin_settlement != snow_island & barutin_settlement != greenwich_island & barutin_settlement != deception_island & barutin_settlement != south_shetland_islands & barutin_settlement != antarctica & barutin_settlement != bulgaria & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & snow_island != bulgaria & greenwich_island != deception_island & greenwich_island != south_shetland_islands & greenwich_island != antarctica & greenwich_island != bulgaria & deception_island != south_shetland_islands & deception_island != antarctica & deception_island != bulgaria & south_shetland_islands != antarctica & south_shetland_islands != bulgaria & antarctica != bulgaria)).
fof(conclusion, conjecture, ? [Cove] : (is_cove(Cove) & located_in(Cove, antarctica) & ? [Place] : (named_after(Cove, Place) & located_in(Place, bulgaria)))).
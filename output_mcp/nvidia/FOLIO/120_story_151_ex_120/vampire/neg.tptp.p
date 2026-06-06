fof(axiom_distinct, axiom, (barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & snow_island != greenwich_island & snow_island != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & greenwich_island != deception_island & greenwich_island != south_shetland_islands & deception_island != south_shetland_islands & south_shetland_islands != antarctica)).

fof(axiom_trans, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).

fof(axiom_barutin_loc_snow, axiom, located_in(barutin_cove, snow_island)).

fof(axiom_snow_loc_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).

fof(axiom_greenwich_loc_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).

fof(axiom_deception_loc_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).

fof(axiom_antarctica_loc_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).

fof(conjecture, conjecture, located_in(barutin_cove, antarctica)).
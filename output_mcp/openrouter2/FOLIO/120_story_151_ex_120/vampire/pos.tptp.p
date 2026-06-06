fof(distinct, axiom, (barutin_cove != snow_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & barutin_cove != greenwich_island & barutin_cove != deception_island & snow_island != south_shetland_islands & snow_island != antarctica & snow_island != greenwich_island & snow_island != deception_island & south_shetland_islands != antarctica & south_shetland_islands != greenwich_island & south_shetland_islands != deception_island & antarctica != greenwich_island & antarctica != deception_island & greenwich_island != deception_island)).
fof(transitivity, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(fact1, axiom, located_in(barutin_cove, snow_island)).
fof(fact2, axiom, located_in(snow_island, south_shetland_islands)).
fof(fact3, axiom, located_in(antarctica, south_shetland_islands)).
fof(goal, conjecture, ~located_in(barutin_cove, antarctica)).
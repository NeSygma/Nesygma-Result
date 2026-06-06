fof(barutin_cove_is_cove, axiom, cove(barutin_cove)).
fof(barutin_cove_named_after_barutin, axiom, named_after(barutin_cove, barutin)).
fof(barutin_is_bulgarian_settlement, axiom, bulgarian_settlement(barutin)).
fof(barutin_cove_in_snow_island, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(antarctica_in_south_shetland, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).
fof(distinct, axiom, (barutin_cove != snow_island & barutin_cove != south_shetland_islands & barutin_cove != antarctica & snow_island != south_shetland_islands & snow_island != antarctica & south_shetland_islands != antarctica)).

fof(negated_conclusion, conjecture, ~ (? [X] : (cove(X) & located_in(X, antarctica) & ? [Y] : (named_after(X, Y) & bulgarian_settlement(Y))))).
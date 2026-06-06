% Negative version: prove Barutin Cove located in Antarctica
fof(distinct_entities, axiom, (barutin_cove != snow_island & barutin_cove != antarctica & snow_island != antarctica)).
fof(premise1, axiom, located_in(barutin_cove, snow_island)).
fof(premise2, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise3, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise4, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise5, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(goal, conjecture, located_in(barutin_cove, antarctica)).
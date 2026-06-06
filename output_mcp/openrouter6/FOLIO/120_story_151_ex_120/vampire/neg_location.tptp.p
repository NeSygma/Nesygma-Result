fof(distinct_constants, axiom, (
    barutin_cove != snow_island &
    barutin_cove != south_shetland_islands &
    barutin_cove != greenwich_island &
    barutin_cove != deception_island &
    barutin_cove != antarctica &
    snow_island != south_shetland_islands &
    snow_island != greenwich_island &
    snow_island != deception_island &
    snow_island != antarctica &
    south_shetland_islands != greenwich_island &
    south_shetland_islands != deception_island &
    south_shetland_islands != antarctica &
    greenwich_island != deception_island &
    greenwich_island != antarctica &
    deception_island != antarctica
)).

fof(premise_2, axiom, located_in(barutin_cove, snow_island)).
fof(premise_3, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise_4a, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise_4b, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise_5, axiom, located_in(antarctica, south_shetland_islands)).
fof(transitivity, axiom, ! [A,B,C] : (located_in(A,B) & located_in(B,C) => located_in(A,C))).

fof(goal, conjecture, located_in(barutin_cove, antarctica)).
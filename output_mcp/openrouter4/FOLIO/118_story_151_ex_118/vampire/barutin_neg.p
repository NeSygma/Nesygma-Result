fof(distinct, axiom, (
    barutin_cove != barutin_settlement &
    barutin_cove != snow_island &
    barutin_cove != greenwich_island &
    barutin_cove != deception_island &
    barutin_cove != south_shetland_islands &
    barutin_cove != antarctica &
    barutin_settlement != snow_island &
    barutin_settlement != greenwich_island &
    barutin_settlement != deception_island &
    barutin_settlement != south_shetland_islands &
    barutin_settlement != antarctica &
    snow_island != greenwich_island &
    snow_island != deception_island &
    snow_island != south_shetland_islands &
    snow_island != antarctica &
    greenwich_island != deception_island &
    greenwich_island != south_shetland_islands &
    greenwich_island != antarctica &
    deception_island != south_shetland_islands &
    deception_island != antarctica &
    south_shetland_islands != antarctica
)).

fof(premise1, axiom, named_after(barutin_cove, barutin_settlement)).

fof(premise2, axiom, located_in(barutin_cove, snow_island)).

fof(premise3a, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise3b, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise3c, axiom, located_in(deception_island, south_shetland_islands)).

fof(premise4, axiom, located_in(antarctica, south_shetland_islands)).

fof(premise5, axiom, ! [A, B, C] : 
    ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).

fof(island_facts, axiom, 
    (island(snow_island) & island(greenwich_island) & island(deception_island))).

fof(negated_conclusion, conjecture, ? [X] : 
    (island(X) & located_in(X, antarctica) & ~named_after(barutin_cove, X))).
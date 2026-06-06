fof(named_after_barutin_cove, axiom, named_after(barutin_cove, barutin_settlement)).
fof(barutin_cove_is_a_cove, axiom, is_a_cove(barutin_cove)).
fof(barutin_cove_in_snow_island, axiom, located_in(barutin_cove, snow_island)).
fof(snow_island_in_south_shetland, axiom, located_in(snow_island, south_shetland_islands)).
fof(greenwich_island_in_south_shetland, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(deception_island_in_south_shetland, axiom, located_in(deception_island, south_shetland_islands)).
fof(south_shetland_is_group_of_islands, axiom, is_a_group_of_islands(south_shetland_islands)).
fof(south_shetland_in_antarctica, axiom, located_in(south_shetland_islands, antarctica)).
fof(transitivity_of_located_in, axiom,
    ! [A, B, C] :
      (located_in(A, B) & located_in(B, C) => located_in(A, C))).

fof(islands_in_antarctica, axiom,
    ! [X] :
      (is_an_island(X) & located_in(X, antarctica) <=>
       (X = snow_island | X = greenwich_island | X = deception_island))).

fof(conclusion_negation, conjecture,
    ~(! [X] :
        (is_an_island(X) & located_in(X, antarctica) => named_after(barutin_cove, X)))).
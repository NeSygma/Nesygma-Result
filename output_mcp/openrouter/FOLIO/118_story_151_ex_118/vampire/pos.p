% Positive version
fof(named_after_bc, axiom, named_after(barutin_cove, barutin_settlement)).
fof(loc_bc_si, axiom, located_in(barutin_cove, snow_island)).
fof(loc_si_sc, axiom, located_in(snow_island, south_chetland_islands)).
fof(loc_gi_sc, axiom, located_in(greenwich_island, south_chetland_islands)).
fof(loc_di_sc, axiom, located_in(deception_island, south_chetland_islands)).
fof(loc_ant_sc, axiom, located_in(antarctica, south_chetland_islands)).
fof(island_snow, axiom, island(snow_island)).
fof(island_green, axiom, island(greenwich_island)).
fof(island_decep, axiom, island(deception_island)).
% Transitivity of located_in
fof(trans_loc, axiom, ! [A,B,C] : ( (located_in(A,B) & located_in(B,C)) => located_in(A,C) ) ).
% Conjecture: Barutin Cove named after all islands in Antarctica
fof(goal, conjecture, ! [X] : ( (island(X) & located_in(X, antarctica)) => named_after(barutin_cove, X) ) ).
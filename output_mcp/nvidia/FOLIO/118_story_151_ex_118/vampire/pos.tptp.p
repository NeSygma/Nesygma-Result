fof(axiom_named_after, axiom, named_after(barutin_cove, barutin)).
fof(axiom_location_sw, axiom, on_southwest_coast_of(barutin_cove, snow_island)).
fof(axiom_loc_snow, axiom, located_in(snow_island, south_shetland_islands)).
fof(axiom_loc_greenwich, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(axiom_loc_deception, axiom, located_in(deception_island, south_shetland_islands)).
fof(axiom_antarctica, axiom, located_in(antarctica, south_shetland_islands)).
fof(axiom_trans, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(conjecture, conjecture, ! [X] : (located_in(X, antarctica) => named_after(barutin_cove, X))).
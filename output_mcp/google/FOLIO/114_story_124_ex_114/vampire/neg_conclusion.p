fof(picuris_in_nm_or_tx, axiom, (mountain_range(picuris) & (located_in(picuris, new_mexico) | located_in(picuris, texas)))).
fof(harding_in_picuris, axiom, (mine(harding) & located_in(harding, picuris))).
fof(harding_donated, axiom, donated(harding)).
fof(no_donated_mines_in_tx_ranges, axiom, ! [M, R] : ((mine(M) & donated(M) & mountain_range(R) & located_in(M, R)) => ~located_in(R, texas))).
fof(conclusion, conjecture, ~located_in(picuris, new_mexico)).
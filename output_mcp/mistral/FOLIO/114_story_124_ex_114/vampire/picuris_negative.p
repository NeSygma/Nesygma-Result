fof(picuris_location, axiom, in_region(picuris_mountains, new_mexico) | in_region(picuris_mountains, texas)).
fof(harding_location, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(harding_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_donated_in_texas, axiom, ! [M] : (in_region(M, texas) => ~(? [Mine] : (located_in(Mine, M) & donated(Mine))))).
fof(conclusion_negation, conjecture, in_region(picuris_mountains, new_mexico)).
fof(distinct_locations, axiom, (new_mexico != texas)).
fof(mountain_range_picuris, axiom, mountain_range_in(picuris, new_mexico) | mountain_range_in(picuris, texas)).
fof(visited_juan, axiom, visited(juan, picuris)).
fof(harding_location, axiom, located_in(harding, picuris) & donated(harding)).
fof(no_donated_mine_in_texas, axiom, ! [M] : (mountain_range_in(M, texas) => ! [N] : (located_in(N, M) => ~donated(N)))).
fof(conclusion, conjecture, ~mountain_range_in(picuris, new_mexico)).
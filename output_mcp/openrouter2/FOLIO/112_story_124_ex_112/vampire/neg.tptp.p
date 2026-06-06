fof(mountain_range_picuris, axiom, mountain_range(picuris)).
fof(picuris_location, axiom, (location(picuris, new_mexico) | location(picuris, texas))).
fof(juan_visited_picuris, axiom, visited(juan, picuris)).
fof(mine_harding, axiom, mine(harding_pegmatite)).
fof(located_harding_picuris, axiom, located_in(harding_pegmatite, picuris)).
fof(donated_harding, axiom, donated(harding_pegmatite)).
fof(no_donated_mines_in_texas, axiom, ! [M] : ((mountain_range(M) & location(M, texas)) => ! [N] : ((mine(N) & located_in(N, M) & donated(N)) => false))).
fof(distinct_constants, axiom, (picuris != new_mexico & picuris != texas & picuris != juan & picuris != harding_pegmatite & new_mexico != texas & new_mexico != juan & new_mexico != harding_pegmatite & texas != juan & texas != harding_pegmatite & juan != harding_pegmatite)).
fof(conjecture, conjecture, ! [M] : ~(visited(juan, M) & mountain_range(M) & location(M, new_mexico))).
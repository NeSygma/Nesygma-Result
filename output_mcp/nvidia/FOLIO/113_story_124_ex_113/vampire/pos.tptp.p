fof(picuris_is_mountain_range, axiom, mountain_range(picuris)).
fof(picuris_in_nm_or_tx, axiom, (in_state(picuris, new_mexico) | in_state(picuris, texas))).
fof(juan_visited_picuris, axiom, visited(juan_de_onate, picuris)).
fof(harding_mine_location, axiom, located_in(harding_pegmatite_mine, picuris)).
fof(harding_mine_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_texas_mountain_range_with_donated_mine, axiom, ! [X] : (mountain_range(X) & in_state(X, texas) => ~ (exists Y : (located_in(Y, X) & donated(Y))))).
fof(goal, conjecture, ? [X] : (visited(juan_de_onate, X) & mountain_range(X) & in_state(X, texas))).
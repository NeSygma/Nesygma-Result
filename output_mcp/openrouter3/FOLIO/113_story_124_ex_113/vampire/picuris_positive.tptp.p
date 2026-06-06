% Premises about Picuris Mountains and related facts
fof(mountain_range_picuris, axiom, mountain_range(picuris_mountains)).
fof(location_picuris, axiom, in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas)).
fof(visited_juan, axiom, visited(juan_de_onate, picuris_mountains)).
fof(mine_harding, axiom, mine(harding_pegmatite_mine)).
fof(located_harding, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(donated_harding, axiom, donated(harding_pegmatite_mine)).
fof(no_donated_mines_in_texas, axiom,
    ! [R] : (mountain_range(R) & in_state(R, texas) => ~? [M] : (mine(M) & located_in(M, R) & donated(M)))).

% Conclusion to evaluate
fof(goal, conjecture, ? [R] : (mountain_range(R) & in_state(R, texas) & visited(juan_de_onate, R))).
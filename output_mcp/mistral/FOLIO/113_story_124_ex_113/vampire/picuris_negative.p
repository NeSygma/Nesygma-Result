fof(picuris_mountain_range, axiom, mountain_range(picuris_mountains)).
fof(picuris_location, axiom, located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas)).
fof(juan_visited_picuris, axiom, visited(juan_de_onate, picuris_mountains)).
fof(harding_mine, axiom, mine(harding_pegmatite_mine)).
fof(harding_located, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(harding_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_donated_mines_in_texas_mr, axiom, 
    ! [M] : (mountain_range(M) & located_in(M, texas) 
             => ~(? [N] : (mine(N) & located_in(N, M) & donated(N))))).
fof(conclusion_negation, conjecture, 
    ! [M] : (mountain_range(M) & located_in(M, texas) => ~visited(juan_de_onate, M))).
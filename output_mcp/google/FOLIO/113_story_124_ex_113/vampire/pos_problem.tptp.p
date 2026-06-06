fof(p1, axiom, (is_in(picuris_mountains, new_mexico) | is_in(picuris_mountains, texas))).
fof(p2, axiom, visited(juan_de_onate, picuris_mountains)).
fof(p3, axiom, (has_mine(picuris_mountains, harding_pegmatite_mine) & donated(harding_pegmatite_mine))).
fof(p4, axiom, ! [M, Mine] : ((is_mountain_range(M) & is_in(M, texas) & has_mine(M, Mine) & donated(Mine)) => $false)).
fof(p5, axiom, is_mountain_range(picuris_mountains)).
fof(goal, conjecture, ? [M] : (visited(juan_de_onate, M) & is_in(M, texas))).
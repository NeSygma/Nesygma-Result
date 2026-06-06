fof(p1, axiom, (mountain_range(picuris_mountains) & (in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas)))).
fof(p2, axiom, visited(juan_de_onate, picuris_mountains)).
fof(p3, axiom, (mine(harding_pegmatite_mine) & in_state(harding_pegmatite_mine, picuris_mountains) & donated(harding_pegmatite_mine))).
fof(p4, axiom, ! [X, M] : ((mountain_range(X) & in_state(X, texas) & mine(M) & in_state(M, X) & donated(M)) => $false)).
fof(goal, conjecture, ~? [X] : (mountain_range(X) & in_state(X, new_mexico) & visited(juan_de_onate, X))).
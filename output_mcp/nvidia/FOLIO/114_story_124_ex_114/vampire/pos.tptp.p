fof(premise1, axiom, mountain_range(picuris_mountains).)).
fof(premise2, axiom, (located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas)).)).
fof(premise3, axiom, visited(juan_de_onate, picuris_mountains).)).
fof(premise4, axiom, located_in(harding_pegmatite_mine, picuris_mountains).)).
fof(premise5, axiom, donated(harding_pegmatite_mine).)).
fof(premise6, axiom, is_mine(harding_pegmatite_mine).)).
fof(premise7, axiom, ! [X] : (mountain_range(X) & located_in(X, texas) => ~? [Y] : (is_mine(Y) & donated(Y) & located_in(Y, X))).)).
fof(conclusion, conjecture, ~? [X] : (mountain_range(X) & located_in(X, new_mexico) & located_in(harding_pegmatite_mine, X)).).
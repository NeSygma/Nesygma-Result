fof(premise1, axiom, mountain_range(picuris_mountains) & (located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas))).
fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).
fof(premise3_1, axiom, mine(harding_pegmatite_mine)).
fof(premise3_2, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise3_3, axiom, donated(harding_pegmatite_mine)).
fof(premise4, axiom, ! [X] : ((mountain_range(X) & located_in(X, texas)) => ~ ? [Y] : (mine(Y) & located_in(Y, X) & donated(Y)))).
fof(conclusion, conjecture, ~ ? [X] : (mountain_range(X) & located_in(X, new_mexico) & visited(juan_de_onate, X))).
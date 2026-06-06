% FOF encoding of premises and negated conclusion
fof(premise_mountain_range, axiom, mountain_range(picuris_mountains)).
fof(premise_location, axiom, (located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas))).
fof(premise_visited, axiom, visited(juan_de_onate, picuris_mountains)).
fof(premise_mine_location, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise_donated, axiom, donated(harding_pegmatite_mine)).
fof(premise_no_mountain_range_texas_mines, axiom, ! [X] : (mountain_range(X) & located_in(X, texas) => ~? [M] : (located_in(M, X) & donated(M)))).
fof(distinct_constants, axiom, (picuris_mountains != new_mexico & picuris_mountains != texas & picuris_mountains != harding_pegmatite_mine & picuris_mountains != juan_de_onate & new_mexico != texas & new_mexico != harding_pegmatite_mine & new_mexico != juan_de_onate & texas != harding_pegmatite_mine & texas != juan_de_onate & harding_pegmatite_mine != juan_de_onate)).
fof(conclusion_neg, conjecture, ? [X] : (mountain_range(X) & located_in(X, new_mexico) & located_in(harding_pegmatite_mine, X))).
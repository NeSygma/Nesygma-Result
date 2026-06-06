% Axioms and negated conjecture
fof(premise1, axiom, mountain_range(picuris_mountains) & (located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas))).
fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).
fof(premise3, axiom, located_in(harding_pegmatite_mine, picuris_mountains) & donated(harding_pegmatite_mine)).
fof(premise4, axiom, ! [X] : ((mountain_range(X) & located_in(X, texas)) => ~ ? [M] : (located_in(M, X) & donated(M)))).
fof(neg_conjecture, conjecture, ! [X] : ~(mountain_range(X) & located_in(X, texas) & visited(juan_de_onate, X))).
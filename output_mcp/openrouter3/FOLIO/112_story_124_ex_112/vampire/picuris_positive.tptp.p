fof(premise_1, axiom, located_in(picuris_mountains, new_mexico) | located_in(picuris_mountains, texas)).
fof(premise_2, axiom, visited(juan_de_onate, picuris_mountains)).
fof(premise_3, axiom, has_mine(picuris_mountains, harding_pegmatite_mine)).
fof(premise_4, axiom, donated(harding_pegmatite_mine)).
fof(premise_5, axiom, ! [M, S, Mi] : ((located_in(M, S) & has_mine(M, Mi) & donated(Mi)) => S != texas)).
fof(goal, conjecture, ? [M] : (visited(juan_de_onate, M) & located_in(M, new_mexico))).
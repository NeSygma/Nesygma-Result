fof(premise1, axiom, mountain_range_in(picuris, new_mexico) | mountain_range_in(picuris, texas)).
fof(premise2, axiom, visited(juan_de_onate, picuris)).
fof(premise3a, axiom, mine_in(harding_pegmatite, picuris)).
fof(premise3b, axiom, donated(harding_pegmatite)).
fof(premise4, axiom, ! [M, X] : (mountain_range_in(M, texas) & mine_in(X, M) => ~donated(X))).
fof(goal, conjecture, ? [M] : (mountain_range_in(M, new_mexico) & visited(juan_de_onate, M))).
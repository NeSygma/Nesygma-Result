% Positive version
fof(distinct_consts, axiom, (picuris_mountains != juan_de_onate & picuris_mountains != harding_pegmatite_mine & juan_de_onate != harding_pegmatite_mine & new_mexico != texas)).

fof(mr_picuris, axiom, mountain_range(picuris_mountains)).
fof(state_disj, axiom, in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas)).
fof(visit_fact, axiom, visited(juan_de_onate, picuris_mountains)).
fof(mine_loc, axiom, mine_location(harding_pegmatite_mine, picuris_mountains)).
fof(mine_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_tx_mine, axiom, ![X,M] : ~ (mountain_range(X) & in_state(X, texas) & mine_location(M,X) & donated(M))).

fof(goal, conjecture, ?[X] : (mountain_range(X) & in_state(X, new_mexico) & visited(juan_de_onate, X))).
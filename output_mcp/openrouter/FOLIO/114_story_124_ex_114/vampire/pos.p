% Positive conjecture (Harding mine not in NM mountain range)
fof(mr_picuris, axiom, mountain_range(picuris)).
fof(loc_picuris, axiom, (in_state(picuris, new_mexico) | in_state(picuris, texas))).
fof(visited_juan, axiom, visited(juan, picuris)).
fof(mine_harding, axiom, mine(harding)).
fof(loc_harding, axiom, located_in(harding, picuris)).
fof(donated_harding, axiom, donated(harding)).
fof(no_tx_mines, axiom, ![X,M] : ((mountain_range(X) & in_state(X, texas) & mine(M) & located_in(M,X) & donated(M)) => $false)).
% distinctness
fof(distinct1, axiom, (picuris != new_mexico & picuris != texas & new_mexico != texas & harding != juan)).
% Conjecture: Harding mine is NOT located in a mountain range in New Mexico
fof(goal, conjecture, ~ ? [X] : (located_in(harding, X) & mountain_range(X) & in_state(X, new_mexico))).
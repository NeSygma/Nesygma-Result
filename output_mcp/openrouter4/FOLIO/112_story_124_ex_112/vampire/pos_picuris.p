% Positive file: original conclusion as conjecture
fof(premise1, axiom, range_in(picuris, nm) | range_in(picuris, tx)).
fof(premise2, axiom, visited(juan, picuris)).
fof(premise3, axiom, mine_in(harding, picuris) & donated(harding)).
fof(premise4, axiom, ! [R, M] : ((range_in(R, tx) & mine_in(M, R) & donated(M)) => $false)).
fof(distinct, axiom, (picuris != harding & picuris != juan & picuris != nm & picuris != tx & harding != juan & harding != nm & harding != tx & juan != nm & juan != tx & nm != tx)).
fof(conclusion, conjecture, ? [R] : (range_in(R, nm) & visited(juan, R))).
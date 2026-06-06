fof(superhero_movie, axiom, superhero_movie(movie_sir_digby)).
fof(named_after, axiom, named_after(movie_sir_digby, sir_digby)).
fof(fight, axiom, fight(sir_digby, nemesis)).
fof(distinct, axiom, (sir_digby != nemesis)).
fof(rule_good_win, axiom, ! [M,P] : ((superhero_movie(M) & good_guy(P) & in_movie(P, M)) => win(P))).
fof(rule_named_good, axiom, ! [M,C] : ((superhero_movie(M) & named_after(M,C)) => good_guy(C))).
fof(rule_named_in, axiom, ! [M,C] : ((superhero_movie(M) & named_after(M,C)) => in_movie(C, M))).
fof(rule_win_fight, axiom, ! [P1,P2] : ((fight(P1,P2) & win(P1)) => ~win(P2))).
fof(conjecture, conjecture, ~win(nemesis)).
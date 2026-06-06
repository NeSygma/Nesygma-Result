fof(superhero_movie_axiom, axiom, superhero_movie(sir_digby_chicken_caesar)).
fof(named_after_axiom, axiom, named_after(sir_digby_chicken_caesar, sir_digby)).
fof(good_guys_win_rule, axiom, ! [M] : (superhero_movie(M) => ? [G] : (in_movie(G, M) & good(G) & wins(G)))).
fof(fight_rule, axiom, ! [X, Y] : (fights(X, Y) => ((good(X) & bad(Y)) | (bad(X) & good(Y))))).
fof(sir_digby_fights_nemesis, axiom, fights(sir_digby, nemesis)).
fof(named_after_good_guy, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => good(C))).
fof(wins_rule, axiom, ! [X, Y] : ((fights(X, Y) & wins(X)) => ~wins(Y))).
fof(named_after_in_movie, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => in_movie(C, M))).
fof(distinct, axiom, (sir_digby != nemesis)).
fof(goal, conjecture, ~wins(nemesis)).
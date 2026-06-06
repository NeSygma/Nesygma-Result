fof(premise_1, axiom, ! [M, X] : ((superhero_movie(M) & good_guy(X) & in_movie(X, M)) => wins(X))).
fof(premise_2, axiom, superhero_movie(the_movie)).
fof(premise_3a, axiom, ! [X, Y] : ((good_guy(X) & bad_guy(Y)) => fights(X, Y))).
fof(premise_3b, axiom, ! [X, Y] : ((bad_guy(X) & good_guy(Y)) => fights(X, Y))).
fof(premise_4, axiom, fights(sir_digby, nemesis)).
fof(premise_5, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => good_guy(C))).
fof(premise_6, axiom, named_after(the_movie, sir_digby)).
fof(premise_7, axiom, ! [X, Y] : ((fights(X, Y) & wins(X)) => ~wins(Y))).
fof(premise_8, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => in_movie(C, M))).
fof(conclusion_neg, conjecture, wins(nemesis)).
fof(sm_sdm, axiom, superhero_movie(sir_digby_movie)).
fof(na_sdm_sd, axiom, named_after(sir_digby_movie, sir_digby)).
fof(nem_rel, axiom, nemesis_of(sir_digbys_nemesis, sir_digby)).
fof(distinct, axiom, sir_digbys_nemesis != sir_digby).

% P1: In superhero movies, the good guys always win.
fof(p1, axiom, ! [X, M] : ((superhero_movie(M) & good_guy(X) & in_movie(X, M)) => wins(X))).

% P3: Good guys fight bad guys and vice versa.
fof(p3a, axiom, ! [X, Y] : ((good_guy(X) & bad_guy(Y)) => fights(X, Y))).
fof(p3b, axiom, ! [X, Y] : ((bad_guy(X) & good_guy(Y)) => fights(X, Y))).

% P4: Sir Digby fights his nemesis.
fof(p4, axiom, fights(sir_digby, sir_digbys_nemesis)).

% P5: If a superhero movie is named after a character, that character is a good guy.
fof(p5, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => good_guy(C))).

% P7: If somebody wins a fight, the person they are fighting does not win.
fof(p7, axiom, ! [X, Y] : ((fights(X, Y) & wins(X)) => ~wins(Y))).

% P8: If a superhero movie is named after a character, that character is in the movie.
fof(p8, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => in_movie(C, M))).

% Conclusion: Sir Digby's nemesis does not win.
fof(goal, conjecture, ~wins(sir_digbys_nemesis)).
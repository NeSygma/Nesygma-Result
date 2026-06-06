% Entities
fof(sir_digby_movie, axiom, superhero_movie(sir_digby_movie)).
fof(sir_digby, axiom, character(sir_digby)).
fof(nemesis, axiom, character(nemesis)).

% Premise 1: In superhero movies, the good guys always win.
fof(p1, axiom, ! [C, M] : ((superhero_movie(M) & good_guy(C) & in_movie(C, M)) => wins(C))).

% Premise 3: Good guys fight bad guys and vice versa.
fof(p3a, axiom, ! [C1, C2, M] : ((superhero_movie(M) & good_guy(C1) & bad_guy(C2) & in_movie(C1, M) & in_movie(C2, M)) => fights(C1, C2))).
fof(p3b, axiom, ! [C1, C2, M] : ((superhero_movie(M) & good_guy(C1) & bad_guy(C2) & in_movie(C1, M) & in_movie(C2, M)) => fights(C2, C1))).

% Premise 4: Sir Digby fights his nemesis.
fof(p4, axiom, fights(sir_digby, nemesis)).

% Premise 5: If a superhero movie is named after a character, that character is a good guy.
fof(p5, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => good_guy(C))).

% Premise 6: The Surprising Adventures of Sir Digby Chicken Caesar is named after Sir Digby.
fof(p6, axiom, named_after(sir_digby_movie, sir_digby)).

% Premise 7: If somebody wins a fight, the person they are fighting does not win.
fof(p7, axiom, ! [X, Y] : ((fights(X, Y) & wins(X)) => ~wins(Y))).

% Premise 8: If a superhero movie is named after a character, that character is in the movie.
fof(p8, axiom, ! [M, C] : ((superhero_movie(M) & named_after(M, C)) => in_movie(C, M))).

% Negated conclusion: Sir Digby's nemesis DOES win.
fof(goal, conjecture, wins(nemesis)).
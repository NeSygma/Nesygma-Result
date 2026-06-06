% Negative version: negated conclusion as conjecture
% Sir Digby's nemesis does NOT not win => Sir Digby's nemesis wins.

% Premise 1: In superhero movies, the good guys always win.
fof(premise_1, axiom, ! [M, P] : 
    ((superhero_movie(M) & good_guy(P) & in_movie(P, M)) => wins(P))).

% Premise 2: The Surprising Adventures of Sir Digby Chicken Caesar is a superhero movie.
fof(premise_2, axiom, superhero_movie(sir_digby_movie)).

% Premise 3: Good guys fight bad guys and vice versa.
fof(premise_3, axiom, ! [X, Y] : 
    ((good_guy(X) & bad_guy(Y)) => fights(X, Y))).
fof(premise_3b, axiom, ! [X, Y] : 
    ((bad_guy(X) & good_guy(Y)) => fights(X, Y))).

% Premise 4: Sir Digby fights his nemesis.
fof(premise_4, axiom, fights(sir_digby, nemesis_of_sir_digby)).

% Premise 5: If a superhero movie is named after a character, that character is a good guy.
fof(premise_5, axiom, ! [M, C] : 
    ((superhero_movie(M) & named_after(M, C)) => good_guy(C))).

% Premise 6: The Surprising Adventures of Sir Digby Chicken Caesar is named after Sir Digby.
fof(premise_6, axiom, named_after(sir_digby_movie, sir_digby)).

% Premise 7: If somebody wins a fight, the person they are fighting does not win.
fof(premise_7, axiom, ! [X, Y] : 
    (wins(X) & fights(X, Y) => ~wins(Y))).

% Premise 8: If a superhero movie is named after a character, that character is in the movie.
fof(premise_8, axiom, ! [M, C] : 
    ((superhero_movie(M) & named_after(M, C)) => in_movie(C, M))).

% Distinctness
fof(distinct, axiom, (sir_digby != nemesis_of_sir_digby & sir_digby != sir_digby_movie & nemesis_of_sir_digby != sir_digby_movie)).

% Negated conclusion: Sir Digby's nemesis wins.
fof(conclusion_neg, conjecture, wins(nemesis_of_sir_digby)).
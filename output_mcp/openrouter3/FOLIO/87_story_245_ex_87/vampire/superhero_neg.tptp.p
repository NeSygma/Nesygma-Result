% Superhero movie problem - Negative version
% Premises
fof(premise_1, axiom, ! [M, G] : (superhero_movie(M) & good_guy(G) & in_movie(M, G) => wins(G))).
fof(premise_2, axiom, superhero_movie(movie)).
fof(premise_3, axiom, ! [G, B] : (good_guy(G) & bad_guy(B) => fights(G, B))).
fof(premise_4, axiom, fights(sir_digby, nemesis)).
fof(premise_5, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => good_guy(C))).
fof(premise_6, axiom, named_after(movie, sir_digby)).
fof(premise_7, axiom, ! [X, Y] : (wins(X) & fights(X, Y) => ~wins(Y))).
fof(premise_8, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => in_movie(M, C))).

% Distinctness axioms
fof(distinct_1, axiom, sir_digby != nemesis).
fof(distinct_2, axiom, movie != sir_digby).
fof(distinct_3, axiom, movie != nemesis).

% Negated conclusion
fof(goal_negated, conjecture, wins(nemesis)).
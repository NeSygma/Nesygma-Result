fof(superhero_movie, axiom, superhero_movie(surprising_adventures)).
fof(named_after_movie, axiom, named_after(surprising_adventures, sir_digby)).
fof(premise5, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => good_guy(C))).
fof(premise3, axiom, ! [X, Y] : (fights(X, Y) => (good_guy(X) & bad_guy(Y)) | (bad_guy(X) & good_guy(Y)))).
fof(premise4, axiom, fights(sir_digby, nemesis)).
fof(premise8, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => in_movie(C, M))).
fof(premise7, axiom, ! [X, Y] : (wins(X, Y) => ~wins(Y, X))).
fof(premise1, axiom, ! [M, C, D] : (superhero_movie(M) & good_guy(C) & bad_guy(D) & fights(C, D) & in_movie(C, M) => wins(C, D))).
fof(conclusion, conjecture, ~wins(nemesis, sir_digby)).
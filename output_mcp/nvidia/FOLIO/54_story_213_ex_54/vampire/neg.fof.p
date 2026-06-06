fof(axiom_romance_ie, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(axiom_romance_related, axiom, ! [X,Y] : ((romance(X) & romance(Y)) => related(X, Y))).
fof(axiom_french_romance, axiom, romance(french)).
fof(axiom_spanish_romance, axiom, romance(spanish)).
fof(axiom_german_related, axiom, related(german, spanish)).
fof(axiom_basque_unrelated, axiom, ! [X] : (X != basque => (~related(basque, X) & ~related(X, basque)))).
fof(goal, conjecture, ~indo_european(french)).
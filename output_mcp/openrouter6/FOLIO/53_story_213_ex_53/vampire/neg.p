fof(all_romance_indo_european, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(romance_languages_related, axiom, ! [X,Y] : ((romance(X) & romance(Y)) => related(X, Y))).
fof(french_romance, axiom, romance(french)).
fof(spanish_romance, axiom, romance(spanish)).
fof(german_related_spanish, axiom, related(german, spanish)).
fof(basque_not_related, axiom, ! [X] : (X != basque => ~related(basque, X))).
fof(goal, conjecture, ~romance(german)).
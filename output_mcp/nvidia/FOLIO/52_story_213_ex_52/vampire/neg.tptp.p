fof(axiom_romance_ie, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(axiom_family, axiom, ! [X,Y] : ((romance(X) & romance(Y)) => related(X, Y))).
fof(axiom_french_romance, axiom, romance(french)).
fof(axiom_spanish_romance, axiom, romance(spanish)).
fof(axiom_german_related_spanish, axiom, related(german, spanish)).
fof(axiom_basque_not_related_any, axiom, ! [X] : ~related(basque, X)).
fof(axiom_basque_not_related_any2, axiom, ! [X] : ~related(X, basque)).
fof(conclusion, conjecture, ~romance(basque)).
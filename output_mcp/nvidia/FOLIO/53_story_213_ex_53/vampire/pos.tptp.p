fof(axiom_1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(axiom_2, axiom, ! [X,Y] : ((romance(X) & romance(Y)) => related(X, Y))).
fof(axiom_3, axiom, romance(french)).
fof(axiom_4, axiom, romance(spanish)).
fof(axiom_5, axiom, related(german, spanish)).
fof(axiom_6, axiom, ! [X] : (~ related(basque, X))).
fof(conjecture, conjecture, romance(german)).
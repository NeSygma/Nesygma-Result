fof(axiom1, axiom, ! [X] : ((romance(X) => indo_european(X)))).
fof(axiom2, axiom, family(romance)).
fof(axiom3, axiom, ! [X] : ((romance(X) => member_of_family(X, romance)))).
fof(axiom4, axiom, ! [X,Y,F] : ((member_of_family(X,F) & member_of_family(Y,F)) => related(X,Y))).
fof(axiom5, axiom, romance(french)).
fof(axiom6, axiom, romance(spanish)).
fof(axiom7, axiom, related(german, spanish)).
fof(axiom8, axiom, ! [Y] : ((Y != basque) => ~related(basque, Y))).
fof(distinctness, axiom, (french != spanish & french != german & spanish != german & basque != french & basque != spanish & basque != german)).
fof(conjecture, conjecture, ~romance(german)).
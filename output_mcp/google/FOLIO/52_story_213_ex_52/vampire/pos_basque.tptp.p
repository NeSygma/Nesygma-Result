fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(p2, axiom, ! [X] : (romance(X) => in_family(X, romance_family))).
fof(p3, axiom, ! [F, X, Y] : ((in_family(X, F) & in_family(Y, F)) => related(X, Y))).
fof(p4, axiom, (romance(french) & romance(spanish))).
fof(p5, axiom, related(german, spanish)).
fof(p6, axiom, ! [X] : (related(basque, X) => basque = X)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, romance(basque)).
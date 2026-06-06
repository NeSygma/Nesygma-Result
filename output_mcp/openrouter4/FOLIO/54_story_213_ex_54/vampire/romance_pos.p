fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(p2a, axiom, language_family(romance_family)).
fof(p2b, axiom, ! [X] : (romance(X) => in_family(X, romance_family))).
fof(p3, axiom, ! [X,Y,F] : ((in_family(X,F) & in_family(Y,F)) => related(X,Y))).
fof(p4a, axiom, romance(french)).
fof(p4b, axiom, romance(spanish)).
fof(p5, axiom, related(german, spanish)).
fof(p6, axiom, ! [X] : (basque != X => ~related(basque, X))).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque & romance_family != french & romance_family != spanish & romance_family != german & romance_family != basque)).
fof(goal, conjecture, indo_european(french)).
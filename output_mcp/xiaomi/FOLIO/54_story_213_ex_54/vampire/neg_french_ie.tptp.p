fof(p1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(p2, axiom, language_family(romance_family)).
fof(p3, axiom, ! [X, Y, F] : ((in_family(X, F) & in_family(Y, F) & language_family(F)) => related(X, Y))).
fof(p4, axiom, in_family(french, romance_family)).
fof(p5, axiom, in_family(spanish, romance_family)).
fof(p6, axiom, romance(french)).
fof(p7, axiom, romance(spanish)).
fof(p8, axiom, related(german, spanish)).
fof(p9, axiom, ! [X] : ~related(basque, X)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, ~indo_european(french)).
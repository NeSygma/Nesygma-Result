fof(premise_1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(premise_2, axiom, language_family(romance_family)).
fof(premise_2b, axiom, ! [X] : (romance(X) => in_family(X, romance_family))).
fof(premise_3, axiom, ! [X, Y, F] : ((in_family(X, F) & in_family(Y, F) & language_family(F)) => related(X, Y))).
fof(premise_4a, axiom, romance(french)).
fof(premise_4b, axiom, romance(spanish)).
fof(premise_5, axiom, related(german, spanish)).
fof(premise_6, axiom, ! [X] : ~related(basque, X)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, indo_european(french)).
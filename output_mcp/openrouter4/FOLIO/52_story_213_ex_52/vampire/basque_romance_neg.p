fof(premise_1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(premise_2_3, axiom, ! [X, Y] : ((romance(X) & romance(Y)) => related(X, Y))).
fof(premise_4a, axiom, romance(french)).
fof(premise_4b, axiom, romance(spanish)).
fof(premise_5, axiom, related(german, spanish)).
fof(premise_6, axiom, ! [X] : (related(basque, X) => X = basque)).
fof(distinct_constants, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(conclusion_neg, conjecture, ~romance(basque)).
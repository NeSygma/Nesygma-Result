fof(distinct_entities, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(premise_1, axiom, ! [X] : (romance_language(X) => indo_european(X))).
fof(premise_2, axiom, ! [X,Y] : ((romance_language(X) & romance_language(Y)) => related(X, Y))).
fof(premise_4, axiom, romance_language(french)).
fof(premise_4b, axiom, romance_language(spanish)).
fof(premise_5, axiom, related(german, spanish)).
fof(premise_6, axiom, ! [X] : (X != basque => ~related(basque, X))).
fof(goal_neg, conjecture, ~indo_european(french)).
fof(premise_1, axiom, ! [X] : (romance_language(X) => indo_european(X))).
fof(premise_2, axiom, language_family(romance)).
fof(premise_3, axiom, ! [F, X, Y] : ((language_family(F) & in_family(X, F) & in_family(Y, F)) => related(X, Y))).
fof(premise_4a, axiom, romance_language(french)).
fof(premise_4b, axiom, romance_language(spanish)).
fof(premise_5, axiom, related(german, spanish)).
fof(premise_6, axiom, ! [X] : (X != basque => ~related(basque, X))).
fof(distinct_languages, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal_negation, conjecture, ~romance_language(german)).
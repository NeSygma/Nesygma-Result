% Negative file: Basque is NOT a Romance language
fof(distinct_languages, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(premise_1, axiom, ! [X] : (romance_language(X) => indo_european(X))).
fof(premise_2_family, axiom, language_family(romance)).
fof(premise_2_in_family, axiom, ! [X] : (romance_language(X) => in_family(X, romance))).
fof(premise_3, axiom, ! [F, X, Y] : (language_family(F) & in_family(X, F) & in_family(Y, F) & X != Y => related_to(X, Y))).
fof(premise_4_french, axiom, romance_language(french)).
fof(premise_4_spanish, axiom, romance_language(spanish)).
fof(premise_5, axiom, related_to(german, spanish)).
fof(premise_6, axiom, ! [X] : (X != basque => ~related_to(basque, X))).
fof(goal_negation, conjecture, ~romance_language(basque)).
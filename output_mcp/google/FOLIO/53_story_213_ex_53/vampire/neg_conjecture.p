fof(romance_to_indo, axiom, ! [X] : (romance_language(X) => indo_european_language(X))).
fof(romance_is_family, axiom, ! [X] : (romance_language(X) => in_family(X, romance_family))).
fof(family_related, axiom, ! [L1, L2] : ((in_family(L1, romance_family) & in_family(L2, romance_family)) => related(L1, L2))).
fof(french_spanish_romance, axiom, (romance_language(french) & romance_language(spanish))).
fof(german_related_spanish, axiom, related(german, spanish)).
fof(basque_not_related, axiom, ! [X] : (X != basque => ~related(basque, X))).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, ~romance_language(german)).
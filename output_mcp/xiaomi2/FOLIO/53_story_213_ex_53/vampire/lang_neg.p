fof(romance_ie, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(romance_family_exists, axiom, language_family(romance_family)).
fof(romance_in_family, axiom, ! [X] : (romance(X) => in_family(X, romance_family))).
fof(family_related, axiom, ! [X, Y, F] : ((in_family(X, F) & in_family(Y, F) & language_family(F)) => related(X, Y))).
fof(french_romance, axiom, romance(french)).
fof(spanish_romance, axiom, romance(spanish)).
fof(german_related_spanish, axiom, related(german, spanish)).
fof(basque_not_related, axiom, ! [X] : ~related(basque, X)).
fof(basque_not_related_rev, axiom, ! [X] : ~related(X, basque)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(goal, conjecture, ~romance(german)).
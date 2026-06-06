% Positive version
fof(all_romance_indoeuro, axiom, ![X] : (romance(X) => indo_european(X))).
fof(romance_family_is_family, axiom, language_family(romance_family)).
fof(romance_member, axiom, ![X] : (romance(X) => member(romance_family, X))).
fof(family_related, axiom, ![F,X,Y] : ((member(F,X) & member(F,Y)) => related(X,Y))).
fof(french_romance, axiom, romance(french)).
fof(spanish_romance, axiom, romance(spanish)).
fof(german_related_spanish, axiom, related(german, spanish)).
fof(basque_no_related, axiom, ![X] : (X != basque => ~related(basque, X))).
fof(distinct_consts, axiom, (french != spanish & french != german & french != basque & french != romance_family & spanish != german & spanish != basque & spanish != romance_family & german != basque & german != romance_family & basque != romance_family)).
fof(goal, conjecture, indo_european(french)).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(romance_french, axiom, romance(french)).
fof(romance_spanish, axiom, romance(spanish)).
fof(related_german_spanish, axiom, related(german, spanish)).
fof(sym_related, axiom, ![X,Y] : (related(X,Y) => related(Y,X))).
fof(romance_related, axiom, ![X,Y] : (romance(X) & romance(Y) => related(X,Y))).
fof(basque_not_related, axiom, ![X] : (X != basque => ~related(basque, X))).
fof(goal, conjecture, ~romance(basque)).
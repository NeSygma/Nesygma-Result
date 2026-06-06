fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(belongs_french, axiom, belongs(french, romance)).
fof(belongs_spanish, axiom, belongs(spanish, romance)).
fof(all_related, axiom, ! [X,Y,F] : ((belongs(X,F) & belongs(Y,F)) => related(X,Y))).
fof(romance_indoeuropean, axiom, ! [X] : (belongs(X, romance) => indo_european(X))).
fof(german_related_spanish, axiom, related(german, spanish)).
fof(basque_not_related, axiom, ! [X] : (related(basque, X) => X = basque)).
fof(goal, conjecture, indo_european(french)).
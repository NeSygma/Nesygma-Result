% Positive file: conclusion "Basque is a Romance language"
fof(premise1, axiom, ! [L, F] : (inFamily(L, F) & F = romance_family => indoEuropean(L))).
fof(premise2, axiom, romance_family = romance_family).
fof(premise3, axiom, ! [F, L1, L2] : (inFamily(L1, F) & inFamily(L2, F) => related(L1, L2))).
fof(premise4a, axiom, inFamily(french, romance_family)).
fof(premise4b, axiom, inFamily(spanish, romance_family)).
fof(premise5, axiom, related(german, spanish)).
fof(premise6, axiom, ! [X] : (X != basque => ~related(basque, X))).
fof(distinct1, axiom, french != spanish).
fof(distinct2, axiom, french != german).
fof(distinct3, axiom, french != basque).
fof(distinct4, axiom, spanish != german).
fof(distinct5, axiom, spanish != basque).
fof(distinct6, axiom, german != basque).
fof(goal, conjecture, inFamily(basque, romance_family)).
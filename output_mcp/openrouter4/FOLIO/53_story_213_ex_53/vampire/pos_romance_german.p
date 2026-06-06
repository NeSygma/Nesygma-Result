% Positive run: check if "German is a Romance language" follows from premises
fof(premise1, axiom, ! [X] : (romance(X) => indo_european(X))).
fof(premise2a, axiom, language_family(romance_family)).
fof(premise2b, axiom, ! [X] : (romance(X) <=> in_family(X, romance_family))).
fof(premise3, axiom, ! [F, X, Y] : ((language_family(F) & in_family(X, F) & in_family(Y, F) & X != Y) => related(X, Y))).
fof(premise4a, axiom, romance(french)).
fof(premise4b, axiom, romance(spanish)).
fof(premise5, axiom, related(german, spanish)).
fof(premise6, axiom, ! [X] : (basque != X => ~related(basque, X))).
fof(distinct, axiom, (french != spanish & french != german & french != basque & spanish != german & spanish != basque & german != basque)).
fof(conclusion, conjecture, romance(german)).
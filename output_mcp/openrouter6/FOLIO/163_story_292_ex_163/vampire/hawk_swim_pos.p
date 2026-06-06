fof(premise1, axiom, ! [X] : (hawk(X) => ~swim(X))).
fof(premise2, axiom, ? [X] : (bird(X) & hawk(X))).
fof(conclusion, conjecture, ! [X] : (bird(X) => swim(X))).
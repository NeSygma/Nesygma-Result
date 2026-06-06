fof(premise1, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(premise2, axiom, ? [X] : (bird(X) & hawk(X))).
fof(conclusion, conjecture, ~(! [X] : (bird(X) => swims(X)))).
% Negative test: negation of humans are mammals
fof(premise1, axiom, ? [X] : (mammal(X) & teeth(X))).
fof(premise2, axiom, ! [X] : (platypus(X) => ~teeth(X))).
fof(premise3, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (human(X) => teeth(X))).
fof(neg_conclusion, conjecture, ? [X] : (human(X) & ~mammal(X))).
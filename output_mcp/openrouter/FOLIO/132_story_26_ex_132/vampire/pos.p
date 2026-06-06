fof(p1, axiom, ? [X] : (mammal(X) & teeth(X))).
fof(p2, axiom, ! [X] : (platypus(X) => ~teeth(X))).
fof(p3, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(p4, axiom, ! [X] : (human(X) => teeth(X))).
fof(conj, conjecture, ! [X] : (platypus(X) => (mammal(X) & ~teeth(X)))).
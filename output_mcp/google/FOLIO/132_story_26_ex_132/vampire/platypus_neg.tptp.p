fof(p1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(p2, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(p3, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(p4, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(conclusion, conjecture, ~! [X] : (platypus(X) => (mammal(X) & ~has_teeth(X)))).
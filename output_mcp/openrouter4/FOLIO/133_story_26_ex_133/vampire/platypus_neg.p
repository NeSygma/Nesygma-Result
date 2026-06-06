fof(premise1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(premise2, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(premise3, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (human(X) => has_teeth(X))).
fof(conclusion_neg, conjecture, ? [X] : (platypus(X) & ~reptile(X))).
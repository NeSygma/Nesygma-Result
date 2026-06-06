fof(premise1, axiom, ! [X] : (square(X) => four_sided(X))).
fof(premise2, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(neg_conjecture, conjecture, ? [X] : (square(X) & ~shape(X))).
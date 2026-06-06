fof(premise1, axiom, ! [X] : (square(X) => four_sided(X))).
fof(premise2, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(negated_conclusion, conjecture, ~(! [X] : (square(X) => shape(X)))).
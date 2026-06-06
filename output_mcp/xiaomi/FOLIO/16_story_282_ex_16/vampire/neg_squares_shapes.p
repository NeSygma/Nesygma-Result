fof(premise_1, axiom, ! [X] : (square(X) => four_sided(X))).
fof(premise_2, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(goal, conjecture, ~(! [X] : (square(X) => shape(X)))).
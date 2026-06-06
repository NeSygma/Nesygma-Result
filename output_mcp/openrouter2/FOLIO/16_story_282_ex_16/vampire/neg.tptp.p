fof(prem1, axiom, ! [X] : (square(X) => four_sided(X))).
fof(prem2, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(goal_neg, conjecture, ? [X] : (square(X) & ~shape(X))).
fof(premise_1, axiom, ! [X] : (happy(X) | sad(X))).
fof(premise_2, axiom, ? [X] : happy(X)).
fof(conclusion_neg, conjecture, ~(! [X] : sad(X))).
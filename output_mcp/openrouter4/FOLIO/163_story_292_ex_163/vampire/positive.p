fof(premise_1, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(premise_2, axiom, ? [X] : (bird(X) & hawk(X))).
fof(goal, conjecture, ! [X] : (bird(X) => swims(X))).
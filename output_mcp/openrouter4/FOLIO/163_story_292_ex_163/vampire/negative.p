fof(premise_1, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(premise_2, axiom, ? [X] : (bird(X) & hawk(X))).
fof(goal_negated, conjecture, ? [X] : (bird(X) & ~swims(X))).
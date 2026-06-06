fof(premise1, axiom, ![X] : (hawk(X) => ~swims(X))).
fof(premise2, axiom, ?[X] : (bird(X) & hawk(X))).
fof(goal_neg, conjecture, ?[X] : (bird(X) & ~swims(X))).
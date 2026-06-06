fof(premise1, axiom, ! [X] : (human(X) => mortal(X))).
fof(premise2, axiom, ! [X] : (greek(X) => human(X))).
fof(goal_neg, conjecture, ! [X] : (~greek(X) | ~mortal(X))).
fof(premise_1, axiom, ! [X] : (human(X) => mortal(X))).
fof(premise_2, axiom, ! [X] : (greek(X) => human(X))).
fof(goal, conjecture, ~ ? [X] : (greek(X) & mortal(X))).
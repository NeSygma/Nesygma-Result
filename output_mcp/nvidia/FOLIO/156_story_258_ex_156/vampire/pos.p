fof(human_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(greek_human, axiom, ! [X] : (greek(X) => human(X))).
fof(goal, conjecture, ? [X] : (greek(X) & mortal(X))).
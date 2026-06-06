fof(humans_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(greeks_human, axiom, ! [X] : (greek(X) => human(X))).
fof(goal, conjecture, ? [X] : (greek(X) & mortal(X))).
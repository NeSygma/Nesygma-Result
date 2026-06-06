fof(all_humans_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(all_greeks_humans, axiom, ! [X] : (greek(X) => human(X))).
fof(goal, conjecture, ? [X] : (greek(X) & mortal(X))).
fof(all_humans_mortal, axiom, ![X] : (human(X) => mortal(X))).
fof(all_greeks_human, axiom, ![X] : (greek(X) => human(X))).
fof(conjecture, conjecture, ?[X] : (greek(X) & mortal(X))).
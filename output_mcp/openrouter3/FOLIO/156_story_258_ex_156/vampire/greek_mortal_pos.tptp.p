% Positive file: Original claim as conjecture
fof(all_humans_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(all_greeks_human, axiom, ! [X] : (greek(X) => human(X))).
fof(goal, conjecture, ? [X] : (greek(X) & mortal(X))). % Some Greeks are mortal
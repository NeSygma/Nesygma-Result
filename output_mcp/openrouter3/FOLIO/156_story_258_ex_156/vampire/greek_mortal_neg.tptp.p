% Negative file: Negated claim as conjecture
fof(all_humans_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(all_greeks_human, axiom, ! [X] : (greek(X) => human(X))).
fof(goal_neg, conjecture, ~(? [X] : (greek(X) & mortal(X)))). % No Greeks are mortal
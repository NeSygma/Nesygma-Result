fof(all_humans_are_mortal, axiom, ! [X] : (human(X) => mortal(X))).
fof(all_greeks_are_humans, axiom, ! [X] : (greek(X) => human(X))).
fof(conclusion_negation, conjecture, ~ (? [X] : (greek(X) & mortal(X)))).
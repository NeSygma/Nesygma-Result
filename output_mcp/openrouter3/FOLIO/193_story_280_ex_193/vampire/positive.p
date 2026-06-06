fof(events_exclusive, axiom, ! [X] : (happy(X) <=> ~sad(X))).
fof(at_least_one_happy, axiom, ? [X] : happy(X)).
fof(goal, conjecture, ! [X] : sad(X)).
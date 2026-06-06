fof(premise_1, axiom, ! [X] : (horse(X) => has_hooves(X))).
fof(premise_2, axiom, ! [X] : (human(X) => ~has_hooves(X))).
fof(goal, conjecture, ? [X] : (human(X) & horse(X))).
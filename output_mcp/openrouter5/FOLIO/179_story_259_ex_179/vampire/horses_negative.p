% Negative version: negated claim as conjecture
fof(premise_1, axiom, ! [X] : (horse(X) => has_hooves(X))).
fof(premise_2, axiom, ! [X] : (human(X) => ~has_hooves(X))).
fof(goal_negated, conjecture, ~? [X] : (human(X) & horse(X))).
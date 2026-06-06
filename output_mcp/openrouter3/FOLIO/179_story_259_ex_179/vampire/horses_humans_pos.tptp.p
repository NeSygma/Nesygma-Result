fof(premise1, axiom, ! [X] : (horse(X) => has_hooves(X))).
fof(premise2, axiom, ! [X] : (human(X) => ~has_hooves(X))).
fof(distinct_entities, axiom, (horse != human & human != horse)).
fof(goal, conjecture, ? [X] : (human(X) & horse(X))).
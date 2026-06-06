fof(all_horses_have_hooves, axiom, ! [X] : (horse(X) => has_hooves(X))).
fof(no_humans_have_hooves, axiom, ! [X] : (human(X) => ~has_hooves(X))).
fof(goal, conjecture, ? [X] : (human(X) & horse(X))).
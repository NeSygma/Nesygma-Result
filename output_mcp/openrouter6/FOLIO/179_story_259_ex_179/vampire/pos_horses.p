fof(premise1, axiom, ! [X] : (horse(X) => has_hoof(X))).
fof(premise2, axiom, ! [X] : (human(X) => ~has_hoof(X))).
fof(goal, conjecture, ? [X] : (human(X) & horse(X))).
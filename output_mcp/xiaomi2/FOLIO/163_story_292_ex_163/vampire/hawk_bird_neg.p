fof(hawk_never_swims, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_birds_are_hawks, axiom, ? [X] : (bird(X) & hawk(X))).
fof(goal, conjecture, ? [X] : (bird(X) & ~swims(X))).
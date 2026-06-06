fof(hawk_never_swims, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_birds_are_hawks, axiom, ? [X] : (bird(X) & hawk(X))).
fof(not_all_birds_swim_conjecture, conjecture, ? [X] : (bird(X) & ~swims(X))).
fof(all_hawks_do_not_swim, axiom, ! [X] : (hawk(X) => ~swim(X))).
fof(some_birds_are_hawks, axiom, ? [X] : (bird(X) & hawk(X))).
fof(not_all_birds_swim, conjecture, ? [X] : (bird(X) & ~swim(X))).
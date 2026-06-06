fof(hawk_no_swim, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_birds_hawks, axiom, ? [X] : (bird(X) & hawk(X))).
fof(goal, conjecture, ! [X] : (bird(X) => swims(X))).
% Positive version
fof(p1, axiom, ! [X] : (fir(X) => evergreen(X))).
fof(p2, axiom, ? [X] : (object_of_worship(X) & fir(X))).
fof(goal, conjecture, ? [X] : (evergreen(X) & ~object_of_worship(X))).
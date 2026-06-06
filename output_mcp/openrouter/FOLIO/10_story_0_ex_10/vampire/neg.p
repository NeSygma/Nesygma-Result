% Negative version (negated conclusion)
fof(ax_exhaustive, axiom, ! [X] : (wild_turkey(X) => (eastern(X) | osceola(X) | gould(X) | merriam(X) | rio_grande(X) | ocellated(X)))).
fof(p1, axiom, ~eastern(tom)).
fof(p2, axiom, ~osceola(tom)).
fof(p3, axiom, ~gould(tom)).
fof(p4, axiom, ~merriam(tom)).
fof(p5, axiom, ~rio_grande(tom)).
fof(p6, axiom, wild_turkey(tom)).
fof(goal, conjecture, ~ocellated(tom)).
fof(p1, axiom, ! [X] : (breeding_back(X) => artificial_selection(X))).
fof(p2_ax, axiom, bred_back(heck_cattle)).
fof(p2_res, axiom, resemble(heck_cattle, aurochs)).
fof(p3, axiom, animal(heck_cattle)).
fof(p4, axiom, animal(aurochs)).
fof(p5, axiom, ? [X, Y] : (animal(X) & bred_back(X) & resemble(X, Y) & animal(Y) & extinct(Y))).
fof(distinct, axiom, heck_cattle != aurochs).
fof(goal, conjecture, extinct(aurochs)).
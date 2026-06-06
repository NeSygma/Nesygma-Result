fof(p1, axiom, animal(heck_cattle)).
fof(p2, axiom, animal(aurochs)).
fof(p3, axiom, bred_back(heck_cattle)).
fof(p4, axiom, resemble(heck_cattle, aurochs)).
fof(p5, axiom, ? [X, Y] : (animal(X) & bred_back(X) & extinct(Y) & resemble(X, Y))).
fof(goal, conjecture, extinct(aurochs)).
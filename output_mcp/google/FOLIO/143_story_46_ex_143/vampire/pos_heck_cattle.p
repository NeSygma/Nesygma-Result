fof(p1, axiom, ! [X] : (is_bred_back(X) => (artificial_selection(X) & domestic_animal(X)))).
fof(p2, axiom, is_bred_back(heck_cattle)).
fof(p3, axiom, animal(heck_cattle)).
fof(p4, axiom, animal(aurochs)).
fof(p5, axiom, ? [X] : (animal(X) & is_bred_back(X) & ? [Y] : (extinct(Y) & resemble(X, Y)))).
fof(goal, conjecture, ? [X] : (X = heck_cattle & artificial_selection(X))).
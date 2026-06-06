fof(p1, axiom, ! [X] : (breeding_back(X) => artificial_selection(X))).
fof(p2_exist, axiom, heck_cattle(hc1)).
fof(p2_univ, axiom, ! [X] : (heck_cattle(X) => breeding_back(X))).
fof(p3, axiom, ! [X] : (heck_cattle(X) => animal(X))).
fof(p4, axiom, ! [X] : (aurochs(X) => animal(X))).
fof(p5, axiom, ? [X, Y] : (animal(X) & breeding_back(X) & resemble(X, Y) & extinct(Y))).
fof(goal, conjecture, ? [X] : (heck_cattle(X) & artificial_selection(X))).
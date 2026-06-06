fof(premise1, axiom, ! [X] : (bred_back(X) => artificial_selection(X))).
fof(premise2, axiom, ? [X, Y] : (heck_cattle(X) & bred_back(X) & aurochs(Y) & resemble(X, Y))).
fof(premise3, axiom, ! [X] : (heck_cattle(X) => animal(X))).
fof(premise4, axiom, ! [X] : (aurochs(X) => animal(X))).
fof(premise5, axiom, ? [X, Y] : (animal(X) & bred_back(X) & resemble(X, Y) & extinct(Y))).
fof(conclusion_neg, conjecture, ~(? [X] : (heck_cattle(X) & artificial_selection(X)))).
% Negative version (negated claim)
fof(premise1, axiom, ! [X] : (bred_back(X) => artificial_selection(X))).
fof(premise2, axiom, ? [X] : (heck_cattle(X) & bred_back(X))).
fof(premise3, axiom, ! [X] : (heck_cattle(X) => animal(X))).
fof(premise4, axiom, ! [X] : (aurochs(X) => animal(X))).
fof(premise5, axiom, ? [X] : (animal(X) & bred_back(X) & resembles_extinct(X))).
fof(goal, conjecture, ~(? [X] : (heck_cattle(X) & artificial_selection(X)))).
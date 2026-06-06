fof(premise_1, axiom, bred_back(heck_cattle, aurochs)).
fof(premise_2, axiom, animal(heck_cattle)).
fof(premise_3, axiom, animal(aurochs)).
fof(premise_4, axiom, ? [X, Y] : (animal(X) & bred_back(X, Y) & extinct(Y))).
fof(distinct, axiom, heck_cattle != aurochs).
fof(goal, conjecture, extinct(aurochs)).
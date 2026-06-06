% Premises about Heck cattle and artificial selection
fof(premise_1, axiom, ! [X] : (breeding_back(X) => artificial_selection(X))).
fof(premise_2, axiom, bred_back(heck_cattle)).
fof(premise_3, axiom, heck_cattle(heck_cattle)).
fof(premise_4, axiom, animal(heck_cattle)).
fof(premise_5, axiom, animal(aurochs)).
fof(premise_6, axiom, ? [X] : (bred_back(X) & resemble(X, aurochs))).
fof(premise_7, axiom, ? [X] : (bred_back(X) & ? [Y] : (resemble(X, Y) & extinct(Y)))).

% Negated conclusion: No Heck cattle are artificially selected
fof(goal_neg, conjecture, ~? [X] : (heck_cattle(X) & artificial_selection(X))).
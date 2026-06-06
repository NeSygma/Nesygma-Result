% Premises about breeding back and aurochs
fof(premise_1, axiom, breeding_back(breeding_back_form)).
fof(premise_2, axiom, artificial_selection(breeding_back_form)).
fof(premise_3, axiom, ! [X] : (breeding_back(X) => domestic_animal(X))).
fof(premise_4, axiom, bred_back(heck_cattle)).
fof(premise_5, axiom, resemble(heck_cattle, aurochs)).
fof(premise_6, axiom, animal(heck_cattle)).
fof(premise_7, axiom, animal(aurochs)).
fof(premise_8, axiom, ? [X,Y] : (bred_back(X) & resemble(X, Y) & extinct(Y))).

% Negated conclusion to test
fof(goal_neg, conjecture, ~extinct(aurochs)).
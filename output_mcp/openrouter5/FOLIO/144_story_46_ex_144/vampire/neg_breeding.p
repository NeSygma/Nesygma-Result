% Negative file: negated claim as conjecture
% Premises:

% Breeding back is a form of artificial selection by the deliberate selective breeding of domestic animals.
fof(premise1, axiom, ! [X] : (breeding_back(X) => artificial_selection(X))).

% Heck cattle were bred back in the 1920s to resemble the aurochs.
fof(premise2, axiom, breeding_back(heck_cattle)).
fof(premise2b, axiom, resembles(heck_cattle, aurochs)).

% Heck cattle are animals.
fof(premise3, axiom, animal(heck_cattle)).

% Aurochs are animals.
fof(premise4, axiom, animal(aurochs)).

% Some animals to be bred back resemble extinct animals.
fof(premise5, axiom, ? [X, Y] : (animal(X) & breeding_back(X) & extinct(Y) & animal(Y) & resembles(X, Y))).

% Negated conclusion: Aurochs are NOT extinct.
fof(goal_neg, conjecture, ~extinct(aurochs)).
% Positive version: original claim as conjecture
% Premises:

% Breeding back is a form of artificial selection by the deliberate selective breeding of domestic animals.
fof(premise1, axiom, ! [X] : (breeding_back(X) => artificial_selection(X))).

% Heck cattle were bred back in the 1920s to resemble the aurochs.
fof(premise2, axiom, breeding_back(heck_cattle)).

% Heck cattle are animals.
fof(premise3, axiom, ! [X] : (heck_cattle(X) => animal(X))).

% Aurochs are animals.
fof(premise4, axiom, ! [X] : (aurochs(X) => animal(X))).

% Some animals to be bred back resemble extinct animals.
fof(premise5, axiom, ? [X] : (animal(X) & to_be_bred_back(X) & ? [Y] : (extinct_animal(Y) & resembles(X, Y)))).

% Distinctness (no constants to distinguish here)

% Conclusion: Some Heck cattle are artificially selected.
fof(goal, conjecture, ? [X] : (heck_cattle(X) & artificial_selection(X))).
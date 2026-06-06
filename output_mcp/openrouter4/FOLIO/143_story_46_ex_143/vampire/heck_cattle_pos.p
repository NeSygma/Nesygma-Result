% Positive test: Is the conclusion "Some Heck cattle are artificially selected" entailed?
fof(premise1, axiom, ! [X] : (bred_back(X) => artificial_selection(X))).
fof(premise2, axiom, ? [X] : (heck(X) & bred_back(X))).
fof(premise3, axiom, ! [X] : (heck(X) => animal(X))).
fof(premise4, axiom, ! [X] : (auroch(X) => animal(X))).
fof(premise5, axiom, ? [X] : (animal(X) & bred_back(X) & resembles_extinct(X))).
fof(goal, conjecture, ? [X] : (heck(X) & artificial_selection(X))).
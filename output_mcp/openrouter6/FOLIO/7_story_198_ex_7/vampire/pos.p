fof(premise2, axiom, ? [X] : (animal(X) & occurs_in(monkeypox_virus, X))).
fof(premise3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(goal, conjecture, ? [X] : animal(X)).
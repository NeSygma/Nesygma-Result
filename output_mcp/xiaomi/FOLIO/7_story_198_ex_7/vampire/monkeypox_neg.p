fof(premise_1, axiom, ! [X] : (occurs_in(monkeypox_virus, X) => can_get_monkeypox(X))).
fof(premise_2, axiom, ? [X] : (animal(X) & occurs_in(monkeypox_virus, X))).
fof(premise_3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise_4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise_6, axiom, ! [X] : ((human(X) & get_flu(X)) => feel_tired(X))).
fof(goal, conjecture, ~ ? [X] : animal(X)).
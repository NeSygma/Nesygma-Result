% Negative test: prove there is no animal
fof(occurs_implication, axiom, ! [X] : (occurs_in(monkeypox, X) => may_get_monkeypox(X))).
fof(monkeypox_occurs_animals, axiom, ? [X] : (animal(X) & occurs_in(monkeypox, X))).
fof(human_mammal, axiom, ! [X] : (human(X) => mammal(X))).
fof(mammal_animal, axiom, ! [X] : (mammal(X) => animal(X))).
fof(goal_neg, conjecture, ! [X] : ~animal(X)).
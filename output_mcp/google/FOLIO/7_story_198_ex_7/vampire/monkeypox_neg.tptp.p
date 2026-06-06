fof(mammal_is_animal, axiom, ! [X] : (mammal(X) => animal(X))).
fof(human_is_mammal, axiom, ! [X] : (human(X) => mammal(X))).
fof(virus_in_animals, axiom, ? [X] : (animal(X) & virus_can_occur_in(monkeypox_virus, X))).
fof(goal, conjecture, ~? [X] : animal(X)).
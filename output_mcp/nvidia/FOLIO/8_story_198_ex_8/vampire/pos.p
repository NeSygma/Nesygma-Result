fof(axiom_virus_implies_disease, axiom, ! [X] : (monkeypox_virus_in(X) => has_monkeypox(X))).
fof(axiom_exists_animal_with_virus, axiom, monkeypox_virus_in(mouse)).
fof(axiom_mouse_is_animal, axiom, animal(mouse)).
fof(axiom_humans_are_mammals, axiom, ! [X] : (human(X) => mammal(X))).
fof(axiom_mammals_are_animals, axiom, ! [X] : (mammal(X) => animal(X))).
fof(axiom_symptoms_include_tiredness, axiom, ! [X] : (has_monkeypox(X) => tired(X))).
fof(axiom_flu_causes_tired, axiom, ! [X] : (gets_flu(X) => tired(X))).
fof(conjecture, conjecture, ! [X] : ~gets_flu(X)).
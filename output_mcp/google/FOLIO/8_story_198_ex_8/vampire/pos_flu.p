fof(monkeypox_virus_in_being, axiom, ! [X] : (monkeypox_virus_in(X) => may_get_monkeypox(X))).
fof(monkeypox_virus_in_animals, axiom, ? [A] : (animal(A) & monkeypox_virus_in(A))).
fof(humans_are_mammals, axiom, ! [X] : (human(X) => mammal(X))).
fof(mammals_are_animals, axiom, ! [X] : (mammal(X) => animal(X))).
fof(symptoms_monkeypox, axiom, ! [X] : (get_monkeypox(X) => (fever(X) & headache(X) & muscle_pains(X) & tired(X)))).
fof(flu_symptoms, axiom, ! [X] : (get_flu(X) => tired(X))).
fof(conclusion, conjecture, ! [X] : ~get_flu(X)).
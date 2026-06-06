fof(occurs_monkeypox_rule, axiom, ! [X] : (occurs(monkeypox_virus, X) => gets_monkeypox(X))).
fof(monkeypox_symptoms, axiom, ! [X] : (gets_monkeypox(X) => (has_symptom(X, fever) & has_symptom(X, headache) & has_symptom(X, muscle_pains) & has_symptom(X, tiredness)))).
fof(flu_symptom, axiom, ! [X] : (gets_flu(X) => has_symptom(X, tiredness))).
fof(human_mammal, axiom, ! [X] : (human(X) => mammal(X))).
fof(mammal_animal, axiom, ! [X] : (mammal(X) => animal(X))).
fof(monkeypox_occurs_in_animal, axiom, ? [X] : (animal(X) & occurs(monkeypox_virus, X))).
fof(conjecture, conjecture, ! [X] : ~gets_flu(X)).
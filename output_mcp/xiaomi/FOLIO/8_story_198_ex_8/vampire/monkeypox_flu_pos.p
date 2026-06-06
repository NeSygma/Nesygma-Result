fof(p1, axiom, ! [X] : (being(X) & has_virus(X, monkeypox_virus) => may_get(X, monkeypox))).
fof(p2, axiom, ? [X] : (animal(X) & has_virus(X, monkeypox_virus))).
fof(p3, axiom, ! [X] : (human(X) => mammal(X))).
fof(p4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(p5, axiom, ! [X] : (has_disease(X, monkeypox) => has_symptom(X, fever) & has_symptom(X, headache) & has_symptom(X, muscle_pains) & has_symptom(X, tiredness))).
fof(p6, axiom, ! [X] : (has_disease(X, flu) => has_symptom(X, tiredness))).
fof(p7, axiom, ! [X] : (human(X) => being(X))).
fof(p8, axiom, ! [X] : (animal(X) => being(X))).
fof(goal, conjecture, ! [X] : ~has_disease(X, flu)).